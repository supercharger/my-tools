import shutil,os,sublime, sublime_plugin
def copytree(src, dst, symlinks=False, ignore=None):
	    if not os.path.exists(dst):
	    	os.makedirs(dst)
	    for item in os.listdir(src):
	    	s = os.path.join(src, item)
	    	d = os.path.join(dst, item)
	    	if s.endswith("node_modules"):
	    		continue;

	    	if os.path.isdir(s):
	    		copytree(s, d, symlinks, ignore)
	        else:
	        	shutil.copy2(s, d)

class FreshCommand(sublime_plugin.TextCommand):
	
	def run(self, edit):
		src = "C:/fresh/"
		dst = "C:/dsrv/submission/"
		copytree(src,dst);
