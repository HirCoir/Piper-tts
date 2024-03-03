latest_checkpoint=$(ls -1 /kaggle/working/piper/my-training/lightning_logs | grep version_ | sort -t_ -k2,2n | tail -n 1)
latest_checkpoint_dir="/kaggle/working/piper/my-training/lightning_logs/$latest_checkpoint/checkpoints"
latest_checkpoint_file=$(ls -1 "$latest_checkpoint_dir" | grep 'epoch=[0-9]*-step=[0-9]*\.ckpt' | sort -t= -k2,2n | tail -n 1)
full_checkpoint_path="$latest_checkpoint_dir/$latest_checkpoint_file"

echo "Latest checkpoint found: $full_checkpoint_path"
echo "Starting countdown. Press Ctrl+C to cancel within 5 seconds."

for i in {5..1}; do
    echo -n "$i "
    sleep 1
done

echo -e "\nExecuting Python command."
python3 -m piper_train \
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
