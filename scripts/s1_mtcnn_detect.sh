python_file='./src/s1_mtcnn_detect.py'

images='./data/lfw-results/paths_1_13233_.csv'
save_folder='./data/lfw-results'
height='250'
width='250'

python $python_file --images $images --save_folder $save_folder --height $height --width $width