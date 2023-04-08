#!/usr/bin/python3 
#-------------------------------------------------------------------------------------
#	os_info.py (for Windows or Linux)
#	Creator: Zi_WaF
#	Group: Centre for Cybersecurity (CFC311022)
#	Instructor: J. Lim
#	whatis: os_info.py	Create automation to display the operating system information.
#
#	To run, (for Windows CMD Prompt or Linux Terminal): python os_info.py
#-------------------------------------------------------------------------------------
# platform - access information of the underlying platform (operating system).
# socket - information on IP Addresses.
# subprocess - used to run new codes and applications by creating new processes.
# sys - used to exit the program.
# os - allows to interact and get Operating System information.
# shutil - disk_usage method tells the disk usage statistics about the given path as a named tuple with the attributes total, used and free.
import platform,socket,subprocess,sys,os,shutil

def OSV_IP(host_os):		# OS, Version, IP Addresses (Private,Public,Default Gateway) for Windows or Linux.
	if host_os == "Windows":		# for Windows Machine
		OS = subprocess.getoutput("systeminfo | findstr /C:\"OS Name\" | for /f \"tokens=3,*\" %i in ('more') do @echo %i %j")
		version = subprocess.getoutput("systeminfo | findstr /C:\"OS Version\" | findstr /V \"BIOS\" | for /f \"tokens=3,*\" %i in ('more') do @echo %i %j")
		cpu_list = subprocess.getoutput("wmic cpu get name, numberofenabledcore | findstr ^0")
		cpu_name = " ".join(cpu_list.strip().split()[:6])
		cpu_proc_enabled = cpu_list.strip().split()[-1]
		cpu_proc_number = 'Enabled: '+ cpu_proc_enabled
		memory_raw = subprocess.getoutput("systeminfo | find \"Total Physical Memory\" | for /f \"tokens=4\" %i in ('more') do @echo %i")
		memory = memory_raw.split(",")[0] + ' GiB'
		private_ip = socket.gethostbyname(socket.gethostname())
		public_ip = subprocess.getoutput("curl -s ifconfig.io")
		default_gateway = subprocess.getoutput("ipconfig | findstr /i \"Gateway\" | findstr ^1 | for /f \"tokens=13\" %i in ('more') do @echo %i")
	elif host_os == "Linux":		# for Linux Machine
		OS=host_os
		version = platform.release()
		cpu_list = subprocess.getoutput("cat /proc/cpuinfo | grep \"model name\" | awk -F: '{print $2}' | uniq -c")
		cpu_name = " ".join(cpu_list.strip().split()[1:])
		cpu_proc_number = cpu_list.strip().split()[0]
		memory_raw = subprocess.getoutput("free -h | grep \"Mem:\" | awk '{print$2}'")
		memory = memory_raw.split("G")[0] + ' GB'
		private_ip = subprocess.getoutput("hostname -I")
		public_ip = subprocess.getoutput("curl -s ifconfig.io")
		default_gateway = subprocess.getoutput("route -n | grep UG | awk '{print $2}'")
	else:							# for Others
		print(f"Operating System: {host_os}")
		print("\n\tScript only works for Windows or Linux Operating System.")
		sys.exit(0)
	# Output the Machine Info (Windows or Linux), Private IP address, Public IP address, and Default Gateway.
	print(f"\nOperating System: {OS}")
	print(f"Version: {version}")
	print(f'CPU: {cpu_name} ({cpu_proc_number} Processors)')
	print(f'Memory: {memory}\n')
	print(f"Private IP Address: {private_ip}")
	print(f"Public IP Address: {public_ip}")
	print(f"Default Gateway: {default_gateway}")
def Disk_Size(host_os):		# Display the Hard Disk Size; Free and Used space.
	if host_os == "Windows":# Disk Size for Windows
		print('\n{:<8}{:<12}{:<12}{:<12}'.format('Disk', 'Size', 'Used', 'Free'))
		print('-' * 40)
		current_drive = os.path.splitdrive(os.getcwd())[0]
		total, used, free = shutil.disk_usage("/")	# Tells the disk usage statistics about the given path as a named tuple with the 
		total = str(total // (2**30)) + " GiB"		# attributes total, used and free where total represents total amount of memory,
		used = str(used // (2**30)) + " GiB"		# used represents used memory and free represents free memory.
		free = str(free // (2**30)) + " GiB"		# Convert to human-readable format.
		print('{:<8}{:<12}{:<12}{:<12}'.format(current_drive, total, used, free))
	else:					# Disk Size for Linux
		print('\n{:<17}{:<8}{:<8}{:<8}'.format('File System', 'Size', 'Used', 'Free'))
		print('-' * 38)
		print(subprocess.getoutput("df -H | grep -w / | awk '{print$1\"\t\",$2\"\t\",$3\"\t\",$4}'")) # df command report file system space usage
def Five_Largest(host_os):	# Display the Top Five (5) Directories and their Size.
	if host_os == "Windows":	# Top 5 largest size folders for Windows
		# Get total size of each folder
		def folder_size(folder_path):
			total_size = 0
			for dirpath, dirnames, filenames in os.walk(folder_path):	# Walk through the folder and files, and calculate the total size of Folder
				for filename in filenames:
					file_path = os.path.join(dirpath, filename)
					total_size += os.path.getsize(file_path)
			return total_size
		# Start from Home, get the name of Folders in it and join as Path
		current_drive = os.path.splitdrive(os.getcwd())[0]				# Get the current drive (e.g. 'C:')
		folders = os.listdir(current_drive+'\\')
		top_list=[]
		for folder in folders:      
			path=current_drive+'\\'+folder								# Attach current drive and folder names as a path
			if os.path.isdir(path):
				try:
					size=int(folder_size(path))							# Calling the function folder_size() to get the total size of folder
					top_list.append((size,folder))						# Relate the size to the folder name
				except FileNotFoundError:								# For missing files
					continue
		# Sort the top 5 largest size Folders
		sorted_list=sorted(top_list, reverse=True)						
		print('\n{:<14}{} (from {})'.format('Size', 'Directory', current_drive+'\\'+'\\'))
		print('-' * 35)
		for size, name in sorted_list[:5]:								# For human-readable size format
			if size < 1024**3:
				size = f"{size/1024**2:.2f} MB"
			else:
				size = f"{size/1024**3:.2f} GiB"
			print('{:<14}{}'.format(size, name))
	else:																# Top 5 largest size folders for Linux
		print('\n{:<8}{:<20}'.format('Size', 'Directory (from Root)'))
		print('-' * 40)
		print(subprocess.getoutput("du -h / 2>/dev/null | sort -nr | head -n 5"))	# Any 'Permission denied' response send to null, only display information that have access
		print('\n{:<8}{:<20}'.format('Size', 'Directory (from Home)'))
		print('-' * 40)
		print(subprocess.getoutput("du -h ~ 2>/dev/null | sort -nr | head -n 5"))	# Any 'Permission denied' response send to null, only display information that have access
def Cpu_Usage(host_os):		# Display the CPU Usage; Refresh every 10 seconds.
	def power_shell():						# Open Powershell Terminal and display CPU Usage for Windows
		ps_command = 'while ($true){cls;Get-Process | Sort-Object CPU -Descending | Where-Object {$_.CPU -gt 1} | ft; Start-Sleep -s 10}'
		command = 'start powershell -NoExit -Command "{}"'.format(ps_command)
		subprocess.call(command, shell=True)
	def linux_top():						# Open new QTerminal and display CPU Usage for Linux
		subprocess.getoutput("qterminal -e top -id 10")
	while True:								# To give more time when processing displayed information
		answer=input("\nDisplay the CPU Usage? [Yes/no]: ")    
		ans=answer.lower()
		if ( ans == "yes" or ans == "y" or ans == "" ):
			print("\n\tDisplaying CPU Usage.....")
			if host_os == "Windows":		# Display CPU Usage for Windows
				power_shell()
				sys.exit(0)
			else:							# Display CPU Usage for Linux
				linux_top()
				sys.exit(0)
		elif ( ans == "no" or ans == "n" ):
			print("\n\tGoodbye.")			# Exit the Program
			sys.exit(0)
		else:								# Any other inputs will return back the loop
			print("Input error. Please try again.")

# Checking the OS of Host
host_os=platform.system().strip()

OSV_IP(host_os)
Disk_Size(host_os)
Five_Largest(host_os)
Cpu_Usage(host_os)


