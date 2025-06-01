from faker import Faker
import os
import sys
import uuid
import rapidjson as json
from upload_to_s3 import upload_to_s3
fake = Faker('en_IN')

# Generate a single random record
def generate_record():
    return {
        'id': str(uuid.uuid4()),
        'name': fake.name(),
        'phone': fake.phone_number(),
        'address': fake.address().replace('\n', ', '),
        'email': fake.email()
    }

# Get folder path from user
def get_output_folder():
    folder = input("Enter the output folder path to save JSON files: ").strip()
    os.makedirs(folder, exist_ok=True)
    return folder
def get_record_count():
    rec_cnt=input("Enter the total records do you want to generate: ").strip()
    return rec_cnt
def get_mb_size():
    mb_size=input("Enter the file size in MB  records do you want to generate: ").strip()
    return mb_size
# Save records into multiple files with ~100MB each
def generate_data(total_records, size_mb,folder_path):
    #max_bytes = max_file_size_mb * 1024 * 1024
    max_bytes = size_mb * 1024 * 1024
    file_index = 1
    current_file_size = 0
    current_file_path = os.path.join(folder_path, f"data_{file_index}.json")
    current_file = open(current_file_path, 'w', encoding='utf-8')

    current_file.write("[\n")  # Start of JSON array
    first_record = True

    for i in range(total_records):
        record = generate_record()
        record_json = json.dumps(record)

        # Add comma between records (but not after the first one)
        if not first_record:
            current_file.write(",\n")
        else:
            first_record = False

        current_file.write(record_json)
        current_file_size += len(record_json.encode('utf-8'))

        if current_file_size >= max_bytes:
            current_file.write("\n]")
            current_file.close()
            print(f"File written: {current_file_path} ({i + 1} records)")

            # Start new file
            file_index += 1
            current_file_path = os.path.join(folder_path, f"data_{file_index}.json")
            current_file = open(current_file_path, 'w', encoding='utf-8')
            current_file.write("[\n")
            current_file_size = 0
            first_record = True

    current_file.write("\n]")
    current_file.close()
    print(f"Final file written: {current_file_path}")
    
    bucket_name = 'vikbuck00909'
    print ("upload starts.......")
    upload_to_s3(output_folder, bucket_name)
    print ("upload Ends.......")

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Usage: python datagenerator.py <record_count>")
        sys.exit(1)
    tc=get_record_count()
    mb=get_mb_size()
    print(tc)
    total_count = int(tc)#int(sys.argv[1])
    size_mb=int(mb)#int(sys.argv[2])
    output_folder = get_output_folder()
    print("Total Count:", total_count)
    print("Size (MB):", size_mb)
    print("output_folder", output_folder)
    generate_data(total_count, size_mb,output_folder)
    #generate_data(total_count, 10,output_folder)
