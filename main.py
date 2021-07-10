import os
import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import selenium.common.exceptions

class Problema:

    def __init__(self,id=None,solutie=None):
        self.id=id
        self.solutie=solutie

    def fac_fisier(self):

        self.director = "problema_"+self.id

        self.parent_dir= "./probleme"

        self.path = os.path.join( self.parent_dir , self.director )

        try:
            os.mkdir(path=self.path)
        except FileExistsError as error:
            print(error)

        try:
            with open(os.path.join(self.path, "solutie_" + self.id+ ".txt" ), 'w') as fisier:
                fisier.write(self.solutie)
        except UnicodeError as error :
            print(error)
            print(self.id)



def id_name_link(link):
    problema_id = ""
    problema_name = ""
    nr = 0
    link = reversed(link)
    for ch in link:
        if (ch == '/'):
            nr = nr + 1
        elif (nr == 0):
            problema_name += ch
        elif (nr == 1):
            problema_id += ch

    problema_name = problema_name[::-1]
    problema_id = problema_id[::-1]

    return (problema_id,problema_name)


class Cont:


    def __init__(self,username,password,path_chrome_driver):

        self.user= username

        self.password = password

        self.path_chrome_driver=path_chrome_driver

        self.driver = webdriver.Chrome(self.path_chrome_driver)

        self.wait = 0.85

    def login(self):

        self.driver.get('https://www.pbinfo.ro/')

        user_box=self.driver.find_element_by_id("user")

        user_box.send_keys(self.user)

        pass_box=self.driver.find_element_by_id("parola")

        pass_box.send_keys(self.password)

        connect_box=self.driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div[4]/div[1]/div[2]/form/div/div[2]/div[4]/button')

        connect_box.click()

        sleep(self.wait*2)


    def take_problems(self):

        self.driver.get('https://www.pbinfo.ro/profil/'+ self.user+'/probleme')
        sleep(self.wait)
        block_probleme = self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[3]/div[2]/div[2]/div[3]/div[1]')
        sleep(self.wait)
        lista_probleme =block_probleme.find_elements_by_tag_name('a')
        lista_probleme_id = []
        lista_probleme_name = []

        for problema in lista_probleme:
            problema_id,problema_name = id_name_link( problema.get_property('href') )
            if(problema.get_attribute('style') == 'color: green;' ):
                lista_probleme_name.append(problema_name)
                lista_probleme_id.append(problema_id)

        for i in range(len(lista_probleme_id)):
            self.driver.get('https://www.pbinfo.ro/?pagina=solutie-oficiala&id='+lista_probleme_id[i])
            sleep(self.wait)

            ok = 1

            try:
                block_solutie = self.driver.find_element_by_css_selector('pre.code_cpp.cm-s-default')
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    block_solutie = self.driver.find_element_by_css_selector('pre.code_c.cm-s-default')
                except selenium.common.exceptions.NoSuchElementException:
                    ok = 0
                    print(lista_probleme_id[i])
            if ok == 1 :

                block_solutie.click()
                sleep(self.wait)
                block_solutie.send_keys(Keys.CONTROL,'a')
                block_solutie.send_keys(Keys.CONTROL,'c')

                solutie = pyperclip.paste()
                PProblema = Problema(lista_probleme_id[i],solutie)

                PProblema.fac_fisier()

                #print(solutie)

        sleep(self.wait)


def main():

    user = input('username : ')
    password = input('password : ')

    cont = Cont(username=user,password=password,path_chrome_driver='./chromedriver.exe')
    cont.login()
    cont.take_problems()


if __name__ == '__main__':
    main()
