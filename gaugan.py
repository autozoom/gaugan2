import requests, re, shutil, os, base64, random, string, sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--style', dest='style')
args = parser.parse_args()

style = args.style

def getUrl():
	print('Getting new server address...')
	r = requests.get('http://gaugan.org/gaugan2/demo.js')
	urls = re.findall(r'\'(http.*?://.*?/)\'', re.search(r'urls=.*?;', r.text)[0])
	return urls[0]

url = getUrl()

for img in os.listdir('./in/'):
	print(f'Processing image \'{img}\'')

	# get b64 encoded image
	with open('./in/' + img, "rb") as f:
		imgb64 = 'data:image/png;base64,' + str(base64.b64encode(f.read()))[2:-1]

	# generate name for requests
	name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

	while True:
		try:
			# send map img to server
			POSTdata = {
				'name': name,
				'masked_segmap': imgb64,
				# 'masked_edgemap': imgb64,
				# 'masked_image': imgb64,
				'style_name': style,
				# 'caption': '',
				'enable_seg': 'true',
				'enable_edge': 'false',
				'enable_caption': 'false',
				'enable_image': 'false',
				'use_model2': 'false'
			}
			resp1 = requests.post(url + 'gaugan2_infer', data = POSTdata)
			print(f'{resp1}')

			# get generated img from server
			POSTdata = {
				'name': name,
			}
			resp2 = requests.post(url + 'gaugan2_receive_output', data = POSTdata, stream = True)
			print(f'{resp2}')
			break
		except Exception as e:
			url = getUrl() # if there is an error getting the image, get a new server URL and try again

	resp2.raw.decode_content = True

	# write image to out folder
	with open('out/' + img.split('.')[0] + '.jpg','wb') as f:
		shutil.copyfileobj(resp2.raw, f)
		

		