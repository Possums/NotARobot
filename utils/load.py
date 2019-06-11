import pickle

f = open('store.pckl', 'rb')
coordinates = pickle.load(f)
f.close()

print(coordinates[0])