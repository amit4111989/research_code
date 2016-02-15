from SdA2 import test_SdA

if __name__=='__main__':

  nins = 300
  nouts = 5
  hidden_layer_sizes = [100,50]
  corruption_levels = [.2,.3]

  test_SdA(nins,nouts,hidden_layer_sizes,corruption_levels,
             finetune_lr=1, pretraining_epochs=75,pretrain_lr=0.001, training_epochs=100,
            batch_size=1)

