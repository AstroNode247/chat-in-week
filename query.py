from pymilvus import connections, utility

conn = connections.connect(host="127.0.0.1", port=19530)


def all_documents():
    return utility.list_collections()
