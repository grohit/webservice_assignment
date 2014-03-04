import uuid
class Member:
	def __init__(self,**argument):
		global idn_cnt
		lid = uuid.uuid4().hex
		idn_cnt=lid[-5:]
		self.member_idn = idn_cnt
		self.name = argument["name"]
		self.gender = argument["gender"]
		self.age = argument["age"]
		self.address = argument["address"]
		self.contact_no = argument["contact_no"]

	def details(self):
		return "Patient Info"+"\n"+"IDN:"+str(self.member_idn)+"\nName:"+self.name+"\nGender"+self.gender+"\nAge"+self.age+"\nAddress"+self.address+"\nContact no"+self.contact_no+"\n"

    

from bottle import request,route, run, template,error
member_dict = {}


@error(404)
def error404(error):
	return "Page not found"

@error(405)
def error405(error):
	return "Method not allowed"	

@error(500)
def error500(error):
	return "Internal Server Error"

@route('/')
@route('/member')
def member_patient():
    return 'member patient is feeling well!'

@route('/member/create',method="POST")
def create_patient():
	name = request.POST['name']
	gender = request.POST['gender']
	age = request.POST['age']
	address = request.POST['address']
	contact_no = request.POST['contact_no']
	mem_obj= Member(name=name,gender=gender,age=age,address=address,contact_no=contact_no)
	member_dict.update({str(mem_obj.member_idn):mem_obj})
	
	return template('<b>Created Patient : IDN {{idn}}</b>!', idn=mem_obj.member_idn)

@route('/member/get/<idn>',method="GET")
def read_details(idn):
	return member_dict[idn].details()

@route('/member/put/<idn>',method="PUT")
def update_details(idn):
	member_idn = request.POST['member_idn']
	if member_idn != idn:
		return "Access Denied"
	member_dict[idn].name = request.POST['name']
	member_dict[idn].gender = request.POST['gender']
	member_dict[idn].age = request.POST['age']
	member_dict[idn].address = request.POST['address']
	member_dict[idn].contact_no = request.POST['contact_no']

	return template("<b>Member patient data Updated : IDN {{idn}}</b>!",idn=member_idn)

@route('/member/del/<idn>',method="DELETE")
def delete_details(idn):
	del(member_dict[idn])
	return template("<b>member patient deleted :IDN {{idn}}",idn=idn)

run(host='localhost', port=8080)


