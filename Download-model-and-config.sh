# Obtener el último checkpoint
latest_checkpoint=$(ls -1 /kaggle/working/piper/my-training/lightning_logs | grep version_ | sort -t_ -k2,2n | tail -n 1)
latest_checkpoint_dir="/kaggle/working/piper/my-training/lightning_logs/$latest_checkpoint/checkpoints"
latest_checkpoint_file=$(ls -1 "$latest_checkpoint_dir" | grep 'epoch=[0-9]*-step=[0-9]*\.ckpt' | sort -t= -k2,2n | tail -n 1)
full_checkpoint_path="$latest_checkpoint_dir/$latest_checkpoint_file"

# Ruta al archivo config.json
config_json_path="/kaggle/working/piper/my-training/config.json"

# Subir el último checkpoint a bashupload.com
upload_checkpoint=$(curl -s https://bashupload.com/ -T "$full_checkpoint_path")
checkpoint_download_url=$(echo "$upload_checkpoint" | grep -o 'https://bashupload.com/[^ ]*')

echo "Uploaded checkpoint. Download URL: $checkpoint_download_url"

# Subir config.json a bashupload.com
upload_config=$(curl -s https://bashupload.com/ -T "$config_json_path")
config_download_url=$(echo "$upload_config" | grep -o 'https://bashupload.com/[^ ]*')

echo "Uploaded config.json. Download URL: $config_download_url"
