python_file='./src/s2_extract_features.py'

images='./data/lfw-results/bounding_boxes_1_13233_.csv'
save_folder='./data/lfw-results/'

python $python_file --images $images --save_folder $save_folder