python_file='./src/s1_mtcnn_detect.py'

images='./data/YoutubeFaces-Subset-Results/paths_1_18824_.csv'
save_folder='./data/YoutubeFaces-Subset-Results'
height='500'
width='500'

python $python_file --images $images --save_folder $save_folder --height $height --width $width