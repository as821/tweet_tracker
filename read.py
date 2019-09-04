def read(url):
    import pickle
    filename = url   # note: no file extension
    pickle_file = open(filename, 'rb')  # rb allows reading from binary file
    storage_struct_read = pickle.load(pickle_file)
    return storage_struct_read