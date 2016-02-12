from SdA import test_SdA

if __name__=='__main__':

  nins = 300
  nouts = 5
  hidden_layer_sizes = [100,75,50]
  trainfile = 'current_benchmarking/train_set.csv'
  testfile = 'current_benchmarking/test_set.csv'
  corruption_levels = [.1,.2,.3]

  test_SdA(nins,nouts,hidden_layer_sizes,trainfile,testfile,corruption_levels,
             finetune_lr=0.1, pretraining_epochs=15,pretrain_lr=0.001, training_epochs=1000,
            batch_size=1)

