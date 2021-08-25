python_file='./src/s3_evaluate_threshold_clustering.py'

input_file1='./data/YoutubeFaces-Subset-Results/features_1_18796_.npy'
labels1='./data/YoutubeFaces-Subset-Results/labels_18796_.npy'

input_file2='./data/IJB-B/512.fea.npy'
labels2='./data/IJB-B/512.labels.npy'

python $python_file $input_file2 --labels_path $labels2