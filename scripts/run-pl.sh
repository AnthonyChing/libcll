python scripts/train.py \
  --do_train \
  --do_predict \
  --strategy FWD \
  --type EXP \
  --model ResNet18 \
  --dataset plcifar10 \
  --lr 1e-4 \
  --batch_size 256 \
  --valid_type Accuracy \
  --output_dir output \
  --noise 1

export CUDA_VISIBLE_DEVICES=0

tensorboard --logdir=output/lightning_logs/ --bind_all