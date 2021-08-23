python_file='./src/s1_mtcnn_detect.py'

images='./data/1-paths/paths_1_13233_.csv'
save_folder='./data/2-faces'
height='720'
width='864'

python $python_file --images $images --save_folder $save_folder --height $height --width $width