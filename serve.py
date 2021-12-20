import io
import re

import pagan
from aiohttp import web
from aiohttp.web_request import Request

L = """
Sed ut perspiciatis unde omnis iste natus error sit voluptatem
accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae
ab illo inventore veritatis et quasi architecto beatae vitae dicta
sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit
aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos
qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui
dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed
quia non numquam eius modi tempora incidunt ut labore et dolore magnam
aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum
exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex
ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in
ea voluptate velit esse quam nihil molestiae consequatur, vel illum
qui dolorem eum fugiat quo voluptas nulla pariatur?

At vero eos et accusamus et iusto odio dignissimos ducimus qui
blanditiis praesentium voluptatum deleniti atque corrupti quos dolores
et quas molestias excepturi sint occaecati cupiditate non provident,
similique sunt in culpa qui officia deserunt mollitia animi, id est
laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita
distinctio. Nam libero tempore, cum soluta nobis est eligendi optio
cumque nihil impedit quo minus id quod maxime placeat facere possimus,
omnis voluptas assumenda est, omnis dolor repellendus. Temporibus
autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe
eveniet ut et voluptates repudiandae sint et molestiae non
recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut
reiciendis voluptatibus maiores alias consequatur aut perferendis
doloribus asperiores repellat.
"""
sentences = list(map(str.strip, re.findall(r'.*?[.?]', ' '.join(L.splitlines()))))
routes = web.RouteTableDef()


@routes.get('/{symbol}/{token_id}')
async def get_metadata(request: Request):
    symbol = request.match_info['symbol']
    token_id = request.match_info['token_id']

    return web.json_response({
        'name': f'{symbol.upper()} #{token_id}',
        'description': sentences[int(token_id) % len(sentences)],
        'image': str(request.url.join(request.app.router['image'].url_for(symbol=symbol, token_id=token_id))),
    })


@routes.get('/{symbol}/{token_id}/_image', name='image')
async def get_image(request: Request):
    avatar = pagan.Avatar(f'{request.match_info["symbol"]}{request.match_info["token_id"]}')
    b = io.BytesIO()
    avatar.img.save(b, 'PNG')

    return web.Response(body=b.getvalue(), headers={'Content-Type': 'image/png'})


def serve():
    app = web.Application()
    app.add_routes(routes)

    web.run_app(app)


if __name__ == '__main__':
    serve()
