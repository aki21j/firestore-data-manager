import firebase_admin
from firebase_admin import credentials, firestore
import sys
import json
import os

def retrieve_data(service_account_file_path, collection_name):
		cred = credentials.Certificate(service_account_file_path)
		firebase_admin.initialize_app(cred)

		store = firestore.client()

		doc_ref = store.collection(collection_name)

		out_data = []

		try:
				docs = doc_ref.get()
				total_docs = len(docs)
				counter = 0
				print("Total docs: {}".format(total_docs))
				for doc in docs:
					if counter == total_docs - 1:
						continue
					counter += 1
					doc_dict = doc.to_dict()

					out_data.append(doc_dict)
				
		except Exception as e:
				print(e)
				
		return out_data

def save_to_file(data_list, collection_name, dump_directory):
		if not os.path.exists(dump_directory):
			os.makedirs(dump_directory)

		out_file_path = os.path.join(dump_directory, collection_name)
		
		with open(out_file_path + '.json', 'w') as outfile:
			json.dump(data_list, outfile, indent=2)

def main():
		service_account_file_path = sys.argv[1]
		collection_name = sys.argv[2]
		dump_directory = sys.argv[3]

		data_list = retrieve_data(service_account_file_path, collection_name)

		if len(data_list) > 0:
				save_to_file(data_list, collection_name, dump_directory)
		else:
				print("No data to dump for collection: {}".format(collection_name))

		print("Fin...")


if __name__ == "__main__":
		main()