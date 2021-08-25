python_file='./src/s3_evaluate_gcn_clustering.py'

input_file='./data/YoutubeFaces-Subset-Results/features_1_18796_.npy'
labels='./data/YoutubeFaces-Subset-Results/labels_18796_.npy'
no_labels='nothing'

input_file2='./data/IJB-B/512.fea.npy'
labels2='./data/IJB-B/512.labels.npy'

knn_graph1='./data/YoutubeFaces-Subset-Results/knn_bt.npy'
knn_graph2='./data/IJB-B/knn.npy'

model_path='./trained_models/gcn.ckpt'

python $python_file --val_feat_path $input_file --val_knn_graph $knn_graph1 --val_label_path $labels --checkpoint $model_path