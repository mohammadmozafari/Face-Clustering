def get_styles():
    styles = """
    
    #wholeWindow {
    }

    #sidebar {
        width: 100px;
        height: 300px;
    }

    #open-folder, #close-folder, #find-faces, #cluster-faces, #exit {
        max-width: 100px;
        max-height: 500px;
        margin: 0px;
        border: none;
        border-radius: 10px;
        background-color: rgb(41, 38, 100);
        height: 120px;
    }
    #close-folder, #exit {
        background-color: rgb(210, 0, 0);
    }
    #open-folder:hover, #find-faces:hover, #cluster-faces:hover {
        background-color: rgb(11, 8, 70);
    }
    #close-folder:hover, #exit:hover {
        background-color: rgb(140, 0, 0);
    }
    #open-folder-btn, #close-folder-btn, #find-faces-btn, #cluster-faces-btn, #exit-btn {
        height: 70px;
        background-color: transparent;
    }
    #open-folder-label, #close-folder-label, #find-faces-label, #cluster-faces-label, #exit-label {
        font-size: 14px;
        color: white;
        background-color: transparent;
    }



    #loading-section {
        padding-left: 10px;
    }

    #mainSection {
    }

    #progressbar {
        color: white;
        font-size: 18px;
        text-align: center;
        max-height: 20px;
        background-color: rgb(178, 179, 180);
        border-radius: 10px;
    }
    #progressbar::chunk {
        background-color: rgb(41, 38, 100);
        border-radius: 8px;
    }

    #content {
        background-color: white;
        border-radius: 10px;
    }

    #tab-head {
        max-height: 30px;
    }
    #btn-frame1, #btn-frame2, #btn-frame3 {
        background-color: rgb(210, 210, 210);
        height: 30px;
        font-size: 18px;
    }
    #btn-frame1 {
        color: white;
        background-color: rgb(41, 38, 100);
        border-top-left-radius: 10px;
        border-right: 1px solid rgb(178, 179, 180);
    }
    #btn-frame2 {
        border-radius: 0px;
        border-right: 1px solid rgb(178, 179, 180);
    }
    #btn-frame3 {
        border-top-right-radius: 10px;
    }
    #tab-frame1, #tab-frame2, #tab-frame3a {
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    #pagination-section {
        max-height: 50px;
        margin-bottom: 20px;
        padding: 0px 500px;
    }
    #prev-btn, #next-btn {
        font-size: 18px;
        color: white;
        padding: 0 5px;
        border-radius: 5px;
        height: 35px;
        background-color: rgb(41, 38, 100);
    }
    #prev-btn:hover, #next-btn:hover {
        background-color: rgb(11, 8, 70);
    }
    #page-input {
        height: 35px;
        border-radius: 5px;
        max-width: 50px;
        border: 1px solid rgb(178, 179, 180);
    }

    """

    return styles
