python_file='./src/s2_create_labels.py'

bboxes='./data/YoutubeFaces-Subset-Results/bounding_boxes_1_18796_.csv'
save_folder='./data/YoutubeFaces-Subset-Results'

python $python_file --bboxes $bboxes --save_folder $save_folder