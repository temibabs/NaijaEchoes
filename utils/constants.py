import io

DEFAULT_MESSAGE = """Hi there! I am"""

CHARACTERS = ["Chinua Achebe", "Wole Soyinka", "Davido",
              "Wizkid", "Burna Boy", "Buchi Emecheta",
              "Don Jazzy", "Peter Obi", "Bola Ahmed Tinubu",
              "Chimamanda Adichie", "Ezra Olubi", "Iyin Aboyeji",
              "Odun Eweniyi"]


def read_image(file_name: str):
    with open(f"avatars/{file_name}", mode="rb") as f:
        return io.BytesIO(f.read())


CHARACTER_AVATARS = {
    "Chinua Achebe": read_image(file_name="Chinua Achebe.jpeg"),
    "Wole Soyinka": read_image(file_name="Wole Soyinka.jpeg"),
    "Bola Ahmed Tinubu": read_image(file_name="Bola Tinubu.jpeg"),
    "Burna Boy": read_image(file_name="Burna Boy.jpeg"),
    "Chimamanda Adichie": read_image(file_name="Chimamanda.jpeg"),
    "Peter Obi": read_image(file_name="Peter Obi.webp"),
    "Davido": read_image(file_name="Davido.jpeg"),
    "Wizkid": read_image(file_name="Wizkid.webp"),
    "Buchi Emecheta": read_image(file_name="Buchi Emecheta.webp"),
    "Don Jazzy": read_image(file_name="Don Jazzy.jpeg"),
    "Ezra Olubi": read_image(file_name="Ezra Olubi.jpeg"),
    "Iyin Aboyeji": read_image(file_name="Iyin Aboyeji.jpeg"),
    "Odun Eweniyi": read_image(file_name="Odun Eweniyi.jpeg")
}
