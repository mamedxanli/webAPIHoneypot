#!/usr/bin/python3

import sys, os, glob, json, subprocess, gzip, time, logging
from influxdb import client as influxdb

# Setting Rest API ID
rest_api_id = 'l0n7wx37ei'
# Setting S3 bucket
s3bucket = 's3://api-honeypot-logs/exportedlogs/'
log_group_name = 'API-Gateway-Execution-Logs_{}/production'.format(rest_api_id)

# Setting DB name
db_name = 'honeypot'
# Setting local json file name
db_json_file = 'db.json'
# Setting root folder for log files
logroot = './logroot'
# Setting AWS region
region = 'us-east-1'

# Setting keys to be fetched from log files
delete_body_key = "Endpoint request body after transformations: "
request_id_key = "Extended Request Id: "
http_method_key = "HTTP Method: "
resource_path_key = "Resource Path: "
user_agent_key = "User-Agent="
ip_key = "X-Forwarded-For="
port_key="X-Forwarded-Port="
delete_status_key = "Method completed with status: "
get_put_body_key = "Method request query string: "
# Creating empty list
all_lines_processed = list()

def file_reader(logroot):
    # This function unzips log files
    filename = str()
    try:
        for filename in glob.iglob(logroot + "/*/*/*", recursive=True):
            if ".gz" in filename:
                with gzip.open(filename, "rb") as f:
                    data = f.read()
                dirname = os.path.dirname(filename)
                newfilename = dirname.split('/')[-1] + '.log'
                with open(dirname + '/' + newfilename, "wb") as file:
                    file.write(data)
    except Exception as ex:
        logging.exception("Failed to gzip file {0}, The error is: {1}".format(filename,ex))

def delete_parser(logfile):
    # This function parses DELETE logs and creates two dictionaries for using in InfluxDB
    delete_dict = {}
    delete_tags = {}
    try:
        with open(logfile, 'r') as f:
            for line in f:
                newlist = line.split()
                timest = line[0:24]
                if http_method_key in line:
                    http_method = line.partition(http_method_key)[-1]
                    http_method_and_path = http_method.replace(http_method_key,'')
                    delete_dict["http_method"] = http_method_and_path.split(",")[0]
                if any (ip_key in x for x in newlist):
                    filter_object = filter(lambda a: ip_key in a, newlist)
                    ip = "".join(filter_object)
                    delete_dict["ip"] = ip.replace(ip_key,'')[:-1]
                if any (port_key in x for x in newlist):
                    filter_object = filter(lambda a: port_key in a, newlist)
                    port = "".join(filter_object)
                    delete_dict["port"] = port.replace(port_key,'')[:-1]
                if delete_body_key in line:
                    body = line.partition(delete_body_key)[-1]
                    delete_dict["body"] = body.replace(delete_body_key,'')[:-1]
                if request_id_key in line:
                    request_id = line.partition(request_id_key)[-1]
                    delete_dict["request_id"] = request_id.replace(request_id_key,'')[:-1]
                if resource_path_key in line:
                    resource_path = line.partition(resource_path_key)[-1]
                    delete_dict["resource_path"] = resource_path.replace(resource_path_key,'')[:-1]
                if delete_status_key in line:
                    status = line.partition(delete_status_key)[-1]
                    delete_dict["status"] = status.replace(delete_status_key,'')[:-1]                
        delete_tags = delete_dict
    except Exception as ex:
        logging.exception("Cannot parse PUT log. The error is: {}".format(ex))
    return timest, delete_dict, delete_tags

def get_parser(logfile):
    # This function parses GET logs and creates two dictionaries for using in InfluxDB
    get_dict = {}
    get_tags = {}
    try:
        with open(logfile, 'r') as f:
            for line in f:
                newlist = line.split()
                timest = line[0:24]
                if any (ip_key in x for x in newlist):
                    filter_object = filter(lambda a: ip_key in a, newlist)
                    ip = "".join(filter_object)
                    get_dict["ip"] = ip.replace(ip_key,'')[:-1]
                if any (port_key in x for x in newlist):
                    filter_object = filter(lambda a: port_key in a, newlist)
                    port = "".join(filter_object)
                    get_dict["port"] = port.replace(port_key,'')[:-1]
                if get_put_body_key in line:
                    body = line.partition(get_put_body_key)[-1]
                    get_dict["body"] = body.replace(get_put_body_key,'')[:-1]
                if request_id_key in line:
                    request_id = line.partition(request_id_key)[-1]
                    get_dict["request_id"] = request_id.replace(request_id_key,'')[:-1]
                get_dict["http_method"] = "GET"
        get_tags = get_dict
    except Exception as ex:
        logging.exception("Cannot parse PUT log. The error is: {}".format(ex))
    return timest, get_dict, get_tags

def put_parser(logfile):
    # This function parses PUT logs and creates two dictionaries for using in InfluxDB
    put_dict = {}
    put_tags = {}
    try:
        with open(logfile, 'r') as f:
            for line in f:
                newlist = line.split()
                timest = line[0:24]
                if any (ip_key in x for x in newlist):
                    filter_object = filter(lambda a: ip_key in a, newlist)
                    ip = "".join(filter_object)
                    put_dict["ip"] = ip.replace(ip_key,'')[:-1]
                if any (port_key in x for x in newlist):
                    filter_object = filter(lambda a: port_key in a, newlist)
                    port = "".join(filter_object)
                    put_dict["port"] = port.replace(port_key,'')[:-1]
                if get_put_body_key in line:
                    body = line.partition(get_put_body_key)[-1]
                    put_dict["body"] = body.replace(get_put_body_key,'')[:-1]
                if request_id_key in line:
                    request_id = line.partition(request_id_key)[-1]
                    put_dict["request_id"] = request_id.replace(request_id_key,'')[:-1]
                put_dict["http_method"] = "PUT"
        put_tags = put_dict
    except Exception as ex:
        logging.exception("Cannot parse PUT log. The error is: {}".format(ex))
    return timest, put_dict, put_tags
    
def build_data_structure(epoch: str, fields: dict = {}, tags: dict = {}, measurement: str = "api_honeypot") -> dict:
    # This function creates a data structure appropriate for InfluxDB
    try:
        # Main dictionary
        data = {
            "measurement" : measurement,
            "time": epoch
        }
        # Nested dictionaries
        data["fields"] = fields
        data["tags"] = tags
        return data
    except Exception as ex:
        logging.exception("Exception while building influx tcp structure: {}".format(ex))

def dbwriter(data):
    # This function write data to Influx DB. Replace arguments for influxdb.InfluxDBClient if necessary
    db_connection = influxdb.InfluxDBClient('172.25.0.12', '8086', 'admin', 'admin123', db_name)
    try:
        db_connection.write_points(data)
    except Exception as ex:
        raise influxdb.InfluxDBClientError("Exception while writing to db: {}".format(ex))
        raise SystemExit()



def main(logroot):
    while True:
        # Setting Log export --from and --to time for AWS logs export
        log_export_start = str(round(time.time() * 1000) - 300000)
        log_export_stop = str(round(time.time() * 1000))
        # Exporting logs
        task_id = subprocess.check_output(['aws logs create-export-task --region {0} --task-name export-to-s3-task --log-group-name {1} --from {2} --to {3} --destination api-honeypot-logs'.format(region,log_group_name, log_export_start, log_export_stop)], shell=True)
        cloudwatch_export_task_id = str(json.loads(task_id.decode('utf-8'))['taskId'])
        # Sync data from S3 to local folder
        subprocess.run(['aws', 's3', 'sync', s3bucket, logroot])
        try:
            file_reader(logroot)
            #Important note: in the following line '*/*' represents the depth of recursive search. Adjust it according to your folder structure
            for filename in glob.iglob(logroot + '*/*/*/*', recursive=True):
                if '.log' in filename:
                    with open(filename, 'r') as f:
                        for line in f:
                            # Determine HTTP method from log file
                            http_method = line.partition(http_method_key)[-1]
                            http_method_and_path = http_method.replace(http_method_key,'')
                            result = http_method_and_path.split(",")[0]
                            # Put each log file through corresponding functions and build data structure
                            if result == "DELETE":
                                delete_epoch, delete_fields, delete_tags = delete_parser(filename)
                                all_lines_processed.append(build_data_structure(delete_epoch, delete_fields, delete_tags, db_name))
                            if "PUT" in line:
                                put_epoch, put_fields, put_tags = put_parser(filename)
                                all_lines_processed.append(build_data_structure(put_epoch, put_fields, put_tags, db_name))
                            if "GET" in line:
                                get_epoch, get_fields, get_tags = get_parser(filename)
                                all_lines_processed.append(build_data_structure(get_epoch, get_fields, get_tags, db_name))
            # Write to local file
            with open(db_json_file, 'w') as dbfile:
                json.dump(all_lines_processed, dbfile)
            # Write to InfluxDB
            dbwriter(all_lines_processed)
            try:
                # Delete the export task if it is still running
                subprocess.run(['aws', 'logs', 'cancel-export-task', '--region', region, '--task-id', cloudwatch_export_task_id])
            except Exception as ex:
                logging.exception("There is no running export task. Error is: {}".format(ex))
        except Exception as ex:
            logging.exception("Cannot run the main function. The error is: {}".format(ex))
        continue

if __name__ == "__main__":
    main(logroot)
