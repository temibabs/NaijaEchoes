import io

DEFAULT_MESSAGE = """Hi there! I am"""


def read_image(file_name: str):
    with open(f"avatars/{file_name}", mode="rb") as f:
        return io.BytesIO(f.read())


CHARACTER_AVATARS = {
    "Bola Ahmed Tinubu": read_image(file_name="Bola Tinubu.jpeg"),
    "Buchi Emecheta": read_image(file_name="Buchi Emecheta.webp"),
    "Burna Boy": read_image(file_name="Burna Boy.jpeg"),
    "Chimamanda Adichie": read_image(file_name="Chimamanda.jpeg"),
    "Chinua Achebe": read_image(file_name="Chinua Achebe.jpeg"),
    "Davido": read_image(file_name="Davido.jpeg"),
    "Don Jazzy": read_image(file_name="Don Jazzy.jpeg"),
    "Ezra Olubi": read_image(file_name="Ezra Olubi.jpeg"),
    "Iyin Aboyeji": read_image(file_name="Iyin Aboyeji.jpeg"),
    "Odun Eweniyi": read_image(file_name="Odun Eweniyi.jpeg"),
    "Peter Obi": read_image(file_name="Peter Obi.webp"),
    "Wizkid": read_image(file_name="Wizkid.webp"),
    "Wole Soyinka": read_image(file_name="Wole Soyinka.jpeg"),
    "Yele Bademosi": read_image(file_name="Yele Bademosi.jpeg")
}

CHARACTERS = CHARACTER_AVATARS.keys()
