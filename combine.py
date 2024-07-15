
shadow_file = "shadow.txt"
shadow_lines = open(shadow_file, "r").readlines()
output_file = "output.txt"
out_writer = open(output_file, "w")
# open all .txt files
for password in shadow_lines:
    password_file = password.split(":")[0] + ".txt"
    with open(password_file, "r") as file:
        out_writer.write(password_file + "\n")
        out_writer.write(file.read())
        out_writer.write("\n")