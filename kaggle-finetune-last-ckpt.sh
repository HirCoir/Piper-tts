latest_checkpoint=$(ls -1 /kaggle/working/piper/my-training/lightning_logs | grep version_ | sort -t_ -k2,2n | tail -n 1)
latest_checkpoint_dir="/kaggle/working/piper/my-training/lightning_logs/$latest_checkpoint/checkpoints"
latest_checkpoint_file=$(ls -1 "$latest_checkpoint_dir" | grep 'epoch=[0-9]*-step=[0-9]*\.ckpt' | sort -t= -k2,2n | tail -n 1)
full_checkpoint_path="$latest_checkpoint_dir/$latest_checkpoint_file"

echo "Latest checkpoint path: $full_checkpoint_path"

read -p "¿Deseas continuar con este checkpoint? (Y/N): " confirmation

if [ "$confirmation" == "Y" ] || [ "$confirmation" == "y" ]; then
    echo "Empezando a entrenar en:"
    
    for ((i=5; i>=1; i--)); do
        echo "$i..."
        sleep 2
    done

    %cd /kaggle/working/piper/src/python
    !python3 -m piper_train \
        --dataset-dir /kaggle/working/piper/my-training \
        --accelerator 'gpu' \
        --devices 1 \
        --batch-size 9 \
        --validation-split 0.0 \
        --num-test-examples 0 \
        --max_epochs 20000 \
        --resume_from_checkpoint "$full_checkpoint_path" \
        --checkpoint-epochs 1 \
        --precision 32
else
    echo "Entrenamiento cancelado."
fi
