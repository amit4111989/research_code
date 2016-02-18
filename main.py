from SdA2 import test_SdA

if __name__=='__main__':

  nins = 300
  nouts = 2
  hidden_layer_sizes = [100,100]
  corruption_levels = [.3,.3]

  test_SdA(nins,nouts,hidden_layer_sizes,corruption_levels,dataset='mnist.pkl.gz',
             finetune_lr=0.1, pretraining_epochs=10,pretrain_lr=0.001, training_epochs=1000,
            batch_size=1)

