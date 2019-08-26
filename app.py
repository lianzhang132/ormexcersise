from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
app = Flask(__name__)
app.config["SECRET_KEY"] = "fjkdjfkdfjdk"
CSRFProtect(app)

# 链接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:666666@127.0.0.1:3306/flask'
# 打印sql语句
app.config['SQLALCHEMY_ECHO'] = True
#设置数据库追踪信息,压制警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 创建数据库对象
db = SQLAlchemy(app)

# 创建模型
class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer,primary_key=True)
    role_name = db.Column(db.String(15),unique=True)

    # 设置关系属性,方便查询使用
    # us 角色表的虚拟字段名称
    # User 是要关联的模型名称
    # role 要关联模型对应表的反向引用 ,对应表的虚拟字段
    us = db.relationship('User',backref='role')

    # 重写__repr__方法,方便查看对象输出内容
    def __repr__(self):
        return 'Role:%s' % self.name

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(15),unique=True)
    roles_id = db.Column(db.Integer,db.ForeignKey('roles.role_id'))

    def __repr__(self):
        return 'User:%s' % self.name



@app.route('/')
def hello_world():

    return render_template('helloworld.html')
@app.route('/register')
def register():
    infos = Role.query.all()

    return render_template('register.html',infos=infos)

@app.route('/registerdo',methods=['get','post'])
def registerdo():
    if  request.method == 'POST':
        name = request.form.get('name')
        roles_id = request.form.get('roles_id')
        user = User(user_name=name,roles_id=roles_id)
        db.session.add(user)
        db.session.commit()
        return redirect('/user_list')
    return "添加失败"
@app.route('/user_list')
def userlist():
    infos = User.query.all()
    return render_template('userlist.html',infos=infos)

@app.route('/user_del/<id>')
def userdel(id):
    user = User.query.filter_by(user_id=id).first()
    db.session.delete(user)
    db.session.commit()
    return "删除成功"

@app.route('/roleadd',methods=['get','post'])
def roleadd():
    if request.method == "POST":
        role_name = request.form.get("role_name")
        role = Role(role_name=role_name)
        db.session.add(role)
        db.session.commit()
        return redirect('/rolelist')
    return render_template("roleadd.html")
@app.route('/rolelist')
def rolelist():
    infos = Role.query.all()
    return render_template('rolelist.html',infos=infos)

@app.route('/role_del/<id>')
def roledel(id):
    role = Role.query.filter_by(role_id=id).first()
    db.session.delete(role)
    db.session.commit()
    return "删除成功"
# db.drop_all()
# db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
