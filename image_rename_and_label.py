import os

def rename_files_in_subdirectories(parent_dir):
    # Duyệt qua tất cả các thư mục con trong thư mục cha
    for subdir in os.listdir(parent_dir):
        subdir_path = os.path.join(parent_dir, subdir)

        # Kiểm tra xem subdir_path có phải là thư mục không
        if os.path.isdir(subdir_path):
            # Tạo tên thư mục cha cho việc đổi tên tệp
            parent_dir_name = os.path.basename(parent_dir)

            # Duyệt qua tất cả các tệp trong thư mục con
            for idx, file_name in enumerate(os.listdir(subdir_path)):
                file_path = os.path.join(subdir_path, file_name)

                # Kiểm tra nếu là tệp, không phải thư mục
                if os.path.isfile(file_path):
                    # Tạo tên mới cho tệp
                    file_extension = os.path.splitext(file_name)[1]  # Lấy đuôi tệp
                    new_file_name = f"{subdir}_{idx + 1}{file_extension}"  # Tên mới
                    new_file_path = os.path.join(subdir_path, new_file_name)

                    # Đổi tên tệp
                    os.rename(file_path, new_file_path)
                    print(f"Đã đổi tên {file_name} thành {new_file_name}")

# Ví dụ sử dụng
parent_directory = './sample_images'  # Thư mục cha của bạn
rename_files_in_subdirectories(parent_directory)
