import os

latest_checkpoint = max(os.listdir('/kaggle/working/piper/my-training/lightning_logs'), key=lambda x: int(x.split('_')[-1]))
latest_checkpoint_dir = f"/kaggle/working/piper/my-training/lightning_logs/{latest_checkpoint}/checkpoints"
latest_checkpoint_file = max(
    [f for f in os.listdir(latest_checkpoint_dir) if f.startswith('epoch=') and f.endswith('.ckpt')],
    key=lambda x: int(x.split('=')[1].split('-')[0])
)
full_checkpoint_path = os.path.join(latest_checkpoint_dir, latest_checkpoint_file)

print(f"Latest checkpoint path: {full_checkpoint_path}")

confirmation = input("¿Deseas continuar con este checkpoint? (Y/N): ")
if confirmation.lower() == "y":
    os.chdir("/kaggle/working/piper/src/python")
    !python3 -m piper_train \
        --dataset-dir /kaggle/working/piper/my-training \
        --accelerator 'gpu' \
        --devices 1 \
        --batch-size 9 \
        --validation-split 0.0 \
        --num-test-examples 0 \
        --max_epochs 20000 \
        --resume_from_checkpoint "{full_checkpoint_path}" \
        --checkpoint-epochs 1 \
        --precision 32
else:
    print("Entrenamiento cancelado.")
