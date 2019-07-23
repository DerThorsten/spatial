import os

user_path = os.path.expanduser('~')
paths = {'luca': os.path.join(user_path, 'Downloads/JacksonFischerCollaborators'),
	 'thorsten': '/media/throsten/Data/embl/',
	 'odcf': '/icgc/dkfzlsdf/analysis/B260/projects/spatial_zurich/data'}

for k, v in paths.iteritems():

