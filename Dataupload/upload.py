''' Functionalities for data upload of parascripturals and audiobible'''
import urllib
import csv
import json
import re
import os
import requests
from urllib.parse import quote
from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.schema import CreateSchema

BASE_URL = r"http://127.0.0.1:8000/v2/cms/rest"
# BASE_URL = r"https://api.vachanengine.org/v2/cms/rest"
# BASE_URL = r"https://stagingapi.vachanengine.org/v2/cms/rest"
TOKEN = "<valid_token>"

headers = {"contentType": "application/json",
            "accept": "application/json",
            'Authorization': "Bearer"+" "+ TOKEN
            }

def create_database_schema():
    postgres_host = os.environ.get("VACHAN_POSTGRES_HOST", "localhost")
    postgres_user = os.environ.get("VACHAN_POSTGRES_USER", "postgres")
    postgres_database = os.environ.get("VACHAN_POSTGRES_DATABASE", "vachan_db")
    postgres_password = os.environ.get("VACHAN_POSTGRES_PASSWORD", "secret")
    postgres_port = os.environ.get("VACHAN_POSTGRES_PORT", "5432")
    postgres_schema = os.environ.get("VACHAN_POSTGRES_SCHEMA", "vachan_cms_rest_12")

    #if you want to use a new schema, you can use below code to specify the name.
    # postgres_schema = os.environ.get("VACHAN_POSTGRES_SCHEMA", "<schema_name>"")


    encoded_password = urllib.parse.quote(postgres_password, safe='')

    # Construct the SQLAlchemy PostgreSQL connection URL with schema
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg2://{postgres_user}:{encoded_password}@"
        f"{postgres_host}:{postgres_port}/{postgres_database}"
        f"?options=--search_path={postgres_schema}"
    )

    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
    conn = engine.connect()

    inspector = inspect(engine)
    existing_schemas = inspector.get_schema_names()

    if postgres_schema in existing_schemas:
        print(f"Schema '{postgres_schema}' already exists.")
    else:
        conn.execute(CreateSchema(postgres_schema))
        conn.commit()
        print(f"Schema '{postgres_schema}' created successfully.")


#creating token
# LOGIN_URL = '/v2/user/login'
# SUPER_USER = os.environ.get("VACHAN_SUPER_USERNAME")
# SUPER_PASSWORD = os.environ.get("VACHAN_SUPER_PASSWORD")

# as_data = {
#             "user_email": SUPER_USER,
#             "password": SUPER_PASSWORD
#         }

# def log_in(data):
#     '''test for login feature'''
#     params = f"?user_email={quote(data['user_email'])}&password={quote(data['password'])}"
#     response = requests.get(BASE_URL+LOGIN_URL+params)
#     if response.status_code == 200:
#         assert response.json()['message'] == "Login Succesfull"
#         assert "userId" in response.json()
#         token =  response.json()['token']
#         assert len(token) == 39
#     elif response.status_code == 401:
#         assert response.json()['details'] ==\
#             "The provided credentials are invalid, check for spelling mistakes "+\
#             "in your password or username, email address, or phone number."
#         assert response.json()['error'] == "Authentication Error"
#     return response

# resp = log_in(as_data)
# assert resp.json()['message'] == "Login Succesfull"
# # print("token = ", resp.json()["token"])
# TOKEN = resp.json()["token"]


# headers = {"contentType": "application/json",
#             "accept": "application/json",
#             'Authorization': "Bearer"+" "+ TOKEN
#             }
            
# SOURCEDATA = []
# #upload single data
# def upload_v2_data(input_data,unit_url):
#     ''' upload data t=in v2 format'''
#     response = requests.post(BASE_URL+unit_url, json=input_data,headers=headers)

#     if not response.status_code == 201:
#         print("resp==>",response)
#         print("resp==>",response.json())
#         print("---------------------------------------------------------------------")
#     print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


# def add_resources_v2():
#     '''add resources in v2 format'''
#     # with open('./files/v1-v2_sources.csv','r',encoding="UTF-8") as file:
#     with open('./files/commentarydata_en_BBC_1_commentary.txt','r',encoding="UTF-8") as file:
#         csvreader = csv.reader(file)
#         header = next(csvreader)
#         permission_list = []
#         for table_row in csvreader:
#             # print("table_row[15]:",type(table_row[15]), table_row[15])
#             access_perm = json.loads(table_row[15])
#             # access_perm = table_row[15]  
#             permission_list = [x for x in access_perm]
#             source_inp = {
#             "resourceType": table_row[6],
#             "language": table_row[9],
#             "version": table_row[12],
#             "versionTag": table_row[13],
#             "label": ["latest","published"],
#             "year": table_row[3],
#             "license": table_row[4].upper(),
#             "accessPermissions": permission_list,
#             "metaData": json.loads(table_row[14])
#             # "metaData": table_row[14]
#             }
#             upload_v2_data(source_inp,'/resources')
#             print("Sourcename--->",table_row[2])
#             SOURCEDATA.append(source_inp)





def upload_data(input_data,unit_url):
    '''Upload  data through POST API call'''
    print("Inside data upload")
    response = requests.post(BASE_URL+unit_url, json=input_data,headers=headers)
    if response.status_code == 201:
        print("<<<==============Resource uploaded successfully!==============>>>")
    else:
        print(f"Failed to create resource. Status code: {response.status_code}")
        print("Response details:", response.json())
        print("---------------------------------------------------------------------")




#1: add_licenses
def add_licenses():
    '''Add licenses'''
    with open('files/licenses.csv', 'r', encoding="UTF-8") as file:
        csvreader = csv.reader(file)

        for table_row in csvreader:
            license_inp = {
                "name": table_row[1],
                "code": table_row[0],
                "license": table_row[2],
                "permissions": ["open-access", "derivable", "publishable"]
            }
            print("la", license_inp)
            upload_data(license_inp,'/resources/licenses')




#2: add_versions
def add_versions():
    '''Add versions'''
    with open('files/versions.csv', 'r', encoding="UTF-8") as file:
        csvreader = csv.reader(file) 

        for table_row in csvreader:
            version_inp = {
                "versionAbbreviation": table_row[0],
                "versionName": table_row[1],
                "versionTag": table_row[2].strip('{}'),
                # "metaData": json.loads(table_row[3]) if table_row[3] != 'null' else {}
            }
            upload_data(version_inp, '/resources/versions')




#3:add_resources 
def add_resources():
    '''Add resources'''
    with open('files/resources.csv','r',encoding="UTF-8") as file:

        csvreader = csv.reader(file)
        next(csvreader)

        for table_row in csvreader:
            if not table_row:
                continue

            # print("!!tablerow:",table_row)
            source_inp = {
                "resourceType": table_row[0],
                "language": table_row[1],
                "version": table_row[2],
                "versionTag": table_row[3],
                "label": [table_row[4]],
                "year": table_row[5],
                "license": table_row[6],
                "accessPermissions": [table_row[7]]
            }
            upload_data(source_inp,'/resources')




def book_id_code_mapping(book_id):
    '''Map bible book id to book code'''
    with open('./files/v1bookcodemap.json','r',encoding="UTF-8") as file:
        v1_book_code_json = json.load(file)
    # print(v1_book_code_json)
    return(v1_book_code_json[book_id])




#4: upload_commentary
def upload_commentary(file_path):
    """upload v2 commentaries
    add license, version, source, content"""   
    parsed_data = []
    with open(file_path, 'r', encoding="UTF-8") as file:
        for line in file:
            # print("line:",line)
            fields = line.strip().split('\t')
            if len(fields) == 7:
                parsed_data.append({
                    
                    'reference':{'book':book_id_code_mapping(fields[6]),
                                "chapter": fields[1],
                                "verseNumber": fields[2],
                                "bookEnd":book_id_code_mapping(fields[6]),
                                "chapterEnd":fields[1],
                                "verseEnd": fields[3]},

                    'commentary': fields[4],
                    'active': fields[5] == 't',
                    "sectionType":["commentary-text"]
                })               
    # Extract resource name from the file path
    file_name = file_path.split("/")[-1].split(".")[0]
    resource_name = "_".join(file_name.split("_")[1:]).strip()
    resource_name_pattern = "^[a-zA-Z]+(-[a-zA-Z0-9]+)*_[A-Z]+_[\w.]+_[a-z]+$"
    if not re.match(resource_name_pattern, resource_name):
        print(f"Invalid resource_name: {resource_name}. Does not match the expected pattern.")
        return None, None
    return parsed_data, resource_name




#5: add_vocabularies
def add_vocabularies(file_path):
    # List to store parsed data
    parsed_data = []
    # Extract resource name from the file path
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    resource_name = file_name
    # Open the CSV file for reading
    with open(file_path, 'r', encoding='UTF-8') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Skip rows with metadata
            if 'COPY public.table_11 (word_id, word, details, active) FROM stdin;' in row:
                continue
            # Check if the row has enough elements
            if len(row) != 4:
                print(f"Skipping row: {row}. Expected 4 elements, got {len(row)} elements.")
                continue          
            # Extract relevant columns from the row
            _, word, details, active = row
            try:
                # Convert details JSON string to a dictionary
                details_dict = json.loads(details)
                # Extract "Type" and "definition" from "details"
                type_value = details_dict.get('Type', '')
                definition_value = details_dict.get('definition', '')
                # Create the data entry
                entry = {
                    'word': word,
                    'details': {
                        'type': type_value,
                        'definition': definition_value,
                    },
                    'active': active.lower() == 'true'
                }
                # Append the entry to the list
                parsed_data.append(entry)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in row: {row}")
                print(f"Details column value: {details}")
                print(f"Error details: {e}")
    return parsed_data, resource_name




#6: add_infographic_data-parascriptural
def add_infographic_data():
    '''Get infographic data from text file'''
    parsed_data = []
    with open('files/infographics.txt', 'r',encoding="UTF-8") as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) == 5:
                parsed_data.append({
                    'parascriptId': int(fields[0]),
                    'category':"infographic",
                    'title': fields[1],
                    'reference':{'book':book_id_code_mapping(fields[4]),
                                "chapter": 0,
                                "verseNumber": 0},
                    'link': fields[2],
                    'active': fields[3] == 't'
                })
    return parsed_data




#7: add_bible_video-parascriptural
def upload_v2_project_videos():
    """upload v2 bible project videos
    add license, version, source, content"""   
    TBP_lang_based_contents = {}
    #generate language based content
    with open('files/TBP-content-v2.csv','r',encoding="UTF-8") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for table_row in csvreader:
            references = []
            books = None
            chapter = None
            table_row[2] = table_row[2].lower()
            table_row[2] = table_row[2].strip()
            if table_row[2] in ("ot","nt","","tanak/ot"):
                pass
            elif re.findall(r"(\w+)-(\w+)" ,table_row[2]):
                books = table_row[2].split("-")
            elif re.findall(r"^(\w+)(,\s*\w+)*$",table_row[2]):
                books = table_row[2].split(',')
            else:
                books = [table_row[2]]           
            table_row[3] =  table_row[3].strip()
            if table_row[3] == "":
                chapter=['0']
            elif re.findall(r"^(\d+)\s*to\s*(\d+)$",table_row[3]):
                chapter = table_row[3].split('to')
            else:
                chapter = [table_row[3].strip()]
            temp_ref=None
            if not books is None:
                print("------books:",books,len(books)) 
                print("------chapter:",chapter,chapter[0],chapter[len(chapter)-1],len(chapter)) 
                for buk in books:
                    if len(books) == 1:
                        # for i in range(int(chapter[0]),int(chapter[-1])+1):
                            print("------>int(chapter[0]),int(chapter[-1])+1:",int(chapter[0]),int(chapter[-1])+1)
                            temp_ref = {
                                "book": books[0],
                                "chapter": int(chapter[0]),
                                "bookEnd": books[len(books)-1],
                                "chapterEnd":int(chapter[len(chapter)-1]),
                                "verseEnd": 0
                            }
                            # references.append(temp_ref)
                    else:
                        temp_ref = {
                            "book": buk,
                            "chapter": int(chapter[0]) if chapter else 0,
                            "verseEnd": 0
                        }
                        
                        # temp_ref = {
                        #         "book": buk,
                        #         "chapter": 0,
                        # }
                        # references.append(temp_ref)
            metadata = {"series": table_row[10]}
            print("----------REF:",temp_ref)
            video_inp = {
            "title": table_row[6]+" "+table_row[8],
            "category":"biblevideo",
            "reference": temp_ref,
            "link": table_row[5],
            "description": table_row[7]+" "+table_row[9],
            "metaData": metadata,
            "active": True
            }
            if table_row[1] in TBP_lang_based_contents.keys():
                TBP_lang_based_contents[table_row[1]].append(video_inp)
            else:
                TBP_lang_based_contents[table_row[1]] = [video_inp]
    #upload content
    # exlcude_test_lang = ["printhi"]
    # print("COntent:",TBP_lang_based_contents[0])
    for content in TBP_lang_based_contents:
    # if not content in inlcude_test_lang:
        print("******************************************")
        
        resource_name = content+"_TBP_1_parascriptural"
        print("resourcename----------------->",resource_name)
        resource_url = f"/resources/parascripturals/{resource_name}"
        upload_data(TBP_lang_based_contents[content],resource_url)





#8:upload_audiobible
def upload_audiobible(file_path):
    """Upload audiobible data."""    
    parsed_data = []
    with open(file_path, 'r', encoding="UTF-8") as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) == 6:
                parsed_data.append({
                    'audioId': int(fields[0]),
                    'name' : fields[1],
                    'reference': {
                        'book': book_id_code_mapping(fields[5]),
                        "chapter": 0,
                        "verseNumber": 0
                    },
                    'link': fields[2],
                    'audioFormat': "mp3",
                    "active": True
                })               
    # Extract resource name from the file path
    file_name = file_path.split("/")[-1].split(".")[0]
    resource_name = "_".join(file_name.split("_")[1:]).strip()
    resource_name_pattern = "^[a-zA-Z]+(-[a-zA-Z0-9]+)*_[A-Z]+_[\w.]+_[a-z]+$"
    if not re.match(resource_name_pattern, resource_name):
        print(f"Invalid resource_name: {resource_name}. Does not match the expected pattern.")
        return None, None
    return parsed_data, resource_name





# #9: add_signbible_data
def add_signbible_data(csv_file_path):
    '''Parse sign video data from a CSV file'''
    parsed_data = []
    try:
        with open(csv_file_path, 'r', encoding="UTF-8") as file:
            csv_reader = csv.reader(file, delimiter=';')  # Adjust delimiter here
            # Skip the header row
            next(csv_reader)
            for line_number, line in enumerate(csv_reader, start=2):  # Start from line 2 (header is line 1)
                try:
                    # Check if the line has the correct number of columns
                    if len(line) != 13:  # Adjust this number based on your CSV file structure
                        raise ValueError(f"Invalid number of columns in line {line_number}")                   
                    # Parse each column from the line
                    signvideo_id = int(line[0].strip())
                    title = line[1].strip()
                    description = line[2].strip()
                    
                    # Parse reference data
                    try:
                        reference_data = json.loads(line[3].strip())
                        reference = {
                            "book": reference_data['book'],
                            "chapter": reference_data.get('chapter', 0),
                            "verseNumber": reference_data.get('verseNumber', 0),
                            "bookEnd": reference_data.get('bookEnd', ''),
                            "chapterEnd": reference_data.get('chapterEnd', 0),
                            "verseEnd": reference_data.get('verseEnd', 0)
                        }
                    except KeyError:
                        raise ValueError(f"Reference column does not contain required keys in line {line_number}")
                    except json.JSONDecodeError:
                        raise ValueError(f"Reference column contains invalid JSON format in line {line_number}")
                    
                    ref_start = line[4].strip()
                    ref_end = line[5].strip()
                    link = line[6].strip()
                    metadata = json.loads(line[7].strip())
                    active = line[8].strip().lower() == 'true'
                    created_user = line[9].strip()
                    last_updated_user = line[10].strip()
                    created_at = line[11].strip()
                    last_updated_at = line[12].strip()                    
                    # Append the parsed data to the list
                    parsed_data.append({
                        'signvideo_id': signvideo_id,
                        'title': title,
                        'description': description,
                        'reference': reference,
                        'ref_start': ref_start,
                        'ref_end': ref_end,
                        'link': link,
                        'metadata': metadata,
                        'active': active,
                        'created_user': created_user,
                        'last_updated_user': last_updated_user,
                        'created_at': created_at,
                        'last_updated_at': last_updated_at
                    })
                except ValueError as ve:
                    print(f"Error processing line {line_number}: {ve}")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")

    return parsed_data





#10: add_bible
def add_bible(csv_file_path):
    usfm_list = []
    # Set a higher field size limit
    csv.field_size_limit(100000000)  # Adjust as needed
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Create a CSV reader
            reader = csv.reader(file)
            # Assuming the first row is the header
            header = next(reader)
            print("Header:", header)  # Print the header
            for values in reader:
                # Extract usfm_text from the second column
                usfm_text = values[1]
                # Format usfm_text as in your example and append to the list
                formatted_usfm = f'{{"USFM": "{usfm_text}"}}'
                usfm_list.append(eval(formatted_usfm))
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while processing {csv_file_path}: {str(e)}")
    print("data,", usfm_list)
    return usfm_list







#==========================================================================================================================
# def add_parascriptual(csv_file_path):   #Only use if you want to add new parascriptual.
#     data_list = []
#     try:
#         with open(csv_file_path, 'r', encoding='utf-8') as file:
#             # Create a CSV reader
#             reader = csv.DictReader(file)
#             # Assuming the first row is the header
#             for row in reader:
#                 try:
#                     # Extracting required fields
#                     reference_data = json.loads(row['reference'])
#                     reference = {
#                         "book": reference_data['book'],
#                         "chapter": reference_data.get('chapter', 0),
#                         "verseNumber": reference_data.get('verseNumber', 0),
#                         "bookEnd": reference_data.get('bookEnd', ''),
#                         "chapterEnd": reference_data.get('chapterEnd', 0),
#                         "verseEnd": reference_data.get('verseEnd', 0)
#                     }
#                 except KeyError:
#                     print(f"Error: 'reference' column does not contain required keys in row: {row}")
#                     continue
#                 except json.JSONDecodeError:
#                     print(f"Error: 'reference' column contains invalid JSON format in row: {row}")
#                     continue
#                 # Constructing data dictionary
#                 data = {
#                     "category": row.get('category', ''),
#                     "title": row.get('title', ''),
#                     "description": row.get('description', ''),
#                     "content": row.get('content', ''),
#                     "reference": reference,
#                     "link": row.get('link', ''),
#                     "metaData": json.loads(row.get('metadata', '{}')),
#                     "active": row.get('active', '') == 't'
#                 }
#                 data_list.append(data)

#     except FileNotFoundError:
#         print(f"Error: File '{csv_file_path}' not found.")
#     except Exception as e:
#         print(f"An error occurred while processing {csv_file_path}: {str(e)}")
#     return data_list
# data = add_parascriptual('files4/ml_TBP_1_parascriptural.csv')
# resource_name = 'ml_TBP_1_parascriptural'
# parascript_url = f"/resources/parascripturals/{resource_name}"
# upload_data(data, parascript_url)




#==========================================================================================================================


# add_resources_v2()

try:
    #check whether the schema is there or not.If not , it will create one as mentioned
    # create_database_schema()

    # 1st
    # Add licenses  
    add_licenses()




   
    # 2nd
    # Add  versions 
    add_versions()




    #3rd
    # Add resources
    add_resources()




    #4th
    # Add commentaries
    # file paths to the respective data files
    file_paths = [
        'files/commentarydata_mr_BBC_1_commentary.txt',
        'files/commentarydata_en_BBC_1_commentary.txt',
        'files/commentarydata_en_SBC_2_commentary.txt',
        'files/commentarydata_en_MHCC_1_commentary .txt',
        'files/commentarydata_hi_HINDIIRVN_1_commentary.txt',
        'files/commentarydata_gu_BBC_1_commentary .txt'
    ]
    for file_path in file_paths:
        data, resource_name = upload_commentary(file_path)
        # print("resourcename", resource_name)
        commentary_url = f"/resources/commentaries/{resource_name}"
        upload_data(data, commentary_url)

    

    
    #5th
    #Add vocabularies

    # file paths to the respective data files
    file_paths = [
    'vocabularies/en_EBD_1_vocabulary.csv',
    'vocabularies/hi_IRVD_1_vocabulary.csv',
    'vocabularies/ins_IRV_1_vocabulary.csv',
    ]
    for file_path in file_paths:
        data, resource_name = add_vocabularies(file_path)
        service_url = f"/resources/vocabularies/{resource_name}"
        # print("resourcename----------------->",resource_name)
        upload_data(data, service_url)

    print("Data Uploaded successfully!")





    #6th
    # Add infographic data to parascripturals
    data = add_infographic_data()
    resource_name = 'hi_HI_1_parascriptural'
    parascript_url = f"/resources/parascripturals/{resource_name}"
    upload_data(data, parascript_url)




    #7th
    # Add Bible video data to parascripturals
    upload_v2_project_videos()



    
    #8th
    # Add audio bible
    file_paths = [
    'files/audiobible_bgc_HB_1_audiobible.txt',
    'files/audiobible_pa_IRV_5_audiobible.txt',
    'files/audiobible_hi_IRV_5_audiobible.txt',
    'files/audiobible_kfs_BSV_1_audiobible.txt',
    'files/audiobible_dgo_DSV_1_audiobible.txt',
    'files/audiobible_ory_IRV_5_audiobible.txt'
        ]
    for file_path in file_paths:
        data, resource_name = upload_audiobible(file_path)
        audiobible_url = f"/resources/bible/audios/{resource_name}"
        upload_data(data, audiobible_url)

    


    #9th
    #signbible
    csv_file_path = 'files/ISL.csv'
    data = add_signbible_data(csv_file_path)
    if data:
        resource_name = 'ins_ISL_1_signbiblevideo'
        signbible_url = f"/resources/bible/videos/{resource_name}"
        upload_data(data, signbible_url)




    #10th
    # #To add all bible together

    # def upload_bible_data():
    #     folder_path = 'bible' #folder path to the respective data files
    #     for filename in os.listdir(folder_path):
    #         if filename.endswith('.csv'):
    #             csv_file_path = os.path.join(folder_path, filename)
    #             resource_name = os.path.splitext(filename)[0]
    #             data = add_bible(csv_file_path)
    #             bible_url = f"/resources/bibles/{resource_name}/books"

    #             #By this method you can validate every data from each files
    #             for entry in data:
    #                 try:
    #                     # Add each entry individually and handle errors
    #                     upload_data([entry], bible_url)
    #                     print(f"Success: Data for {resource_name} uploaded successfully.")
    #                 except Exception as e:
    #                     print(f"Failed to upload data for {resource_name}: {str(e)}")
    
    
    
    #To add  bibles seperately 
    def upload_bible_data():
            folder_path = 'bible' #folder path to the respective data files
            for filename in os.listdir(folder_path):
                if filename.endswith('ur_IRV_5_bible.csv'):
                    csv_file_path = os.path.join(folder_path, filename)
                    resource_name = os.path.splitext(filename)[0]
                    data = add_bible(csv_file_path)
                    #resource names available are as_IRV_5_bible,bgc_HB_1_bible,bn_IRV_5.bible,dgo_DSV_1_bible,en_ESV_1_bible,
                    # gu_IRV_5_bible,hi_IRV_5_bible,kfs_BSV_1_bible,kn_IRV_5_bible,ml_IRV_5_bible,mr_IRV_5_bible,
                    # nag_ISV_1_bible,ne_ULB_1_bible,pa_IRV_5_bible,ta_IRV_5_bible,te_IRV_5_bible,ur_IRV_5_bible
                    bible_url = f"/resources/bibles/{resource_name}/books"
                    #By this method you can validate every data from each files
                    for entry in data:
                        try:
                            # Add each entry individually and handle errors
                            upload_data([entry], bible_url)
                            print(f"Success: Data for {resource_name} uploaded successfully.")
                        except Exception as e:
                            print(f"Failed to upload data for {resource_name}: {str(e)}")

    #Call the function to upload data
    # upload_bible_data()

    print("Data Uploaded success uploadedully!")

except Exception as e:
    print(f"An error occurred: {str(e)}")
