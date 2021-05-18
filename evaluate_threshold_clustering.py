from src.utils.clustering import ThresholdClustering

def main():
    tc = ThresholdClustering()
    clusters = tc.find_clusters(['./results/lfw-features/features_1_13233_.csv'])
    for c in clusters:
        print(c)
        print('------------')

if __name__ == "__main__":
    main()