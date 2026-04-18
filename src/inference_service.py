import redis
# "fake" implementation, true implementation out of scope for assignment

# create cells "database"
cells = {}
cells["45762"] = {"modality": "microscope", "type": "osteosarcoma", "species": "human"}
cells["46314"] = {"modality": "microscope", "type": "osteosarcoma", "species": "human"}
cells["1_512v"] = {"modality": "multiphoton", "type": "medium spiny neuron", "species": "mouse"}
cells["8_512v"] = {"modality": "confocal", "type": "protoplasmic astrocyte", "species": "rat"}
cells["5_512v"] = {"modality": "confocal", "type": "protoplasmic astrocyte", "species": "rat"}
cells["1132_512v"] = {"modality": "confocal", "type": "cerebellar basket cell", "species": "rat"}

# take in host and pw, connect to redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# take in image and file name

# export "inferences" as json
r.publish('inferences', json.dumps(cells[filename]))