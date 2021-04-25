from views import Index, About, Contact

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
}
