from SdA2 import test_SdA

if __name__=='__main__':

  nins = 200
  nouts = 5
  hidden_layer_sizes = [75,75]
  corruption_levels = [.3,.3]

  test_SdA(nins,nouts,hidden_layer_sizes,corruption_levels,dataset='mnist.pkl.gz',
             finetune_lr=0.1, pretraining_epochs=100,pretrain_lr=0.3, training_epochs=1000,
            batch_size=1,threshold = 0.33,patience_init=1,layers=2)

