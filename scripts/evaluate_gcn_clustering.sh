python_file='./src/evaluate_gcn_clustering.py'

input_file='./data/IJB-B/512.fea.npy'
labels='./data/IJB-B/512.labels.npy'
knn_graph='./data/IJB-B/knn.graph.512.bf.npy'
model_path='./trained_models/gcn.ckpt'

python $python_file --val_feat_path $input_file --val_knn_graph $knn_graph --val_label_path $labels --checkpoint $model_path 