python_file='./src/s2_extract_features.py'

images='./data/YoutubeFaces-Subset-Results/bounding_boxes_1_18796_.csv'
save_folder='./data/YoutubeFaces-Subset-Results/'

python $python_file --images $images --save_folder $save_folder