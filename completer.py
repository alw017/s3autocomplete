#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import boto3, sys

S3_PREFIX = "s3://"
PREFIX_OFFSET = len(S3_PREFIX)

# TODO write unit tests using pytest, emulate some boto3 client

def s3_path_completer(prefix, bucket_names=[]):
    """
    Takes a string and default list of bucket names, and returns a newline separated list of its possible completions.
    """
    client = boto3.client('s3')
    has_s3_prefix = prefix.startswith(S3_PREFIX)
    bucket_name_end = prefix.find("/", PREFIX_OFFSET) 
    if not has_s3_prefix:
        return S3_PREFIX
    elif has_s3_prefix and bucket_name_end == -1:
        try: 
            response = client.list_buckets()
            buckets = response.get('Buckets', [])
            result = [S3_PREFIX + bucket['Name'] + '/' for bucket in buckets]
            result += [S3_PREFIX + bucket_name + '/' for bucket_name in bucket_names]
        except:
            result = [S3_PREFIX + bucket_name + '/'
                        for bucket_name in bucket_names]
        
        return "\n".join(result)
    else:
        object_prefix = prefix[:bucket_name_end+1] 
        object_name = prefix[bucket_name_end+1:].replace("'",'')
        try: 
            response = client.list_objects_v2(
                Bucket=prefix[PREFIX_OFFSET:bucket_name_end],
                Prefix=object_name,
                Delimiter='/')
        except: # bucket doesn't exist.
            return ""
        
        # get directories
        common_prefixes = response.get('CommonPrefixes', [])
        shared_prefixes = [object_prefix + obj['Prefix'] 
                           for obj in common_prefixes]
    
        # get files
        contents = response.get('Contents', [])
        content = shared_prefixes + [object_prefix + "'" + obj['Key'] + "'"
                                     for obj in contents]

        return "\n".join(content)

def _debug_completer(prefix, response, test_type, *args):
    """
    debug completion method meant for tests.
    """
    prefix_offset = len(S3_PREFIX)
    has_s3_prefix = prefix.startswith(S3_PREFIX)
    object_name_start_index = prefix.find("/", prefix_offset)
    match test_type:
        case "bucket_query": # response expects a list of bucket names.
            output = [S3_PREFIX + bucket + '/' for bucket in response]
            return " ".join(response)
        case "object_query": # response expects a list of object names
            for obj in response:
                end_index = obj.find("/", len(prefix)-object_name_start_index)
                if end_index == -1:
                    pruned.append(prefix[:object_name_start_index + 1] + obj)
                else:
                    pruned.append(prefix[:object_name_start_index + 1] + obj[:end_index+1])
            pruned = list(set(pruned))
            return " ".join(pruned)

if len(sys.argv) == 2:
    prefix = sys.argv[1]
    print(s3_path_completer(prefix))
elif len(sys.argv) == 3:
    prefix = sys.argv[1]
    if len(sys.argv[2]) > 0:
        bucket_list = sys.argv[2].split(" ")
    else: 
        bucket_list = []
    print(s3_path_completer(prefix, bucket_list))
else:
    print(s3_path_completer(""))

