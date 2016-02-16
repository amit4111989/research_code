from SdA2 import test_SdA

if __name__=='__main__':

  nins = 300
  nouts = 3
  hidden_layer_sizes = [75,50]
  corruption_levels = [.3,.3]

  test_SdA(nins,nouts,hidden_layer_sizes,corruption_levels,dataset='mnist.pkl.gz',
             finetune_lr=0.1, pretraining_epochs=30,pretrain_lr=0.001, training_epochs=1000,
            batch_size=1)

