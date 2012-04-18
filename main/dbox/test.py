from dbox_wrapper import DropboxService

def main():
    dbox = DropboxService()
    print(dbox.url)
    raw_input()

    dbox.getToken()
    
    dbox.upload('test/wing.gif')
    print("File uploaded")
    dbox.download('test/testfile_downloaded.gif', 'wing.gif')
    print("File downloaded")

    ref = dbox.shareRef('wing.gif')
    print(ref)
    print(dbox.listFiles('.'))

    #dbox.getRef(ref, 'wing.gif')

main()
