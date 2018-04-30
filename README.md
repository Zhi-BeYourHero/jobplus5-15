# jobplus5-15

* [白昼魅影](https://github.com/Zhi-BeYourHero)
* [海啸](https://github.com/superLam)
* [跬步郎](https://github.com/cactusboy)

#### 项目目录

```python
jobplus5-15
        /jobplus
            /handlers
            /templates
                /static
```

#### 文件路径及说明

```python
jobplus5-15
        /jobplus
            /handlers
            /templates
                /base.html   # 模板
                /CompanyReigster.html  # 企业注册页
                /PersonalRegister.html  #求职者注册页
                /index.html #主页
                /login.html #登录页
                /job.html   # 职位列表页
                /Company.html   #企业列表页
                /static
```

#### fix #28 登录和退出
###### 20180429 
1、修改forms.py文件第22行，将email改为pssword
2、修改front.py第24行，2行（增加import flash），42行，
3、参照教程，修改base.html文件
4、修改front.py 第51行，增加falsh展示

##### 20180429-2
修改冲突文件：forms.py、front.py、macros.html

##### 20180430 
将models.py中的company字段改成company_msg, 相关联的也改了
