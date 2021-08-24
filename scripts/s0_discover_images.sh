python_file='./src/s0_discover_images.py'

images='./data/lfw-results/paths_1_13233_.csv'
pairs_path='./data/lfw-results'
items_in_file='100000'

python $python_file --folder $folder --save_folder $save_folder --items_in_file $items_in_file