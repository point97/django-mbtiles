import logging

from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _

from . import app_settings
from models import MBTiles, MissingTileError, MBTilesNotFoundError


logger = logging.getLogger(__name__)


def tile(request, name, z, x, y, catalog=None):
    """ Serve a single image tile """
    try:
        mbtiles = MBTiles(name, catalog)
        data = mbtiles.tile(z, x, y)
        response = HttpResponse(content_type='image/png')
        response.write(str(data))
        return response
    except MBTilesNotFoundError, e:
        logger.warning(e)
    except MissingTileError:
        logger.warning(_("Tile %s not available in %s") % ((z, x, y), name))
        if not app_settings.MISSING_TILE_404:
            return HttpResponse(content_type="image/png")
    raise Http404


def preview(request, name, catalog=None):
    try:
        mbtiles = MBTiles(name, catalog)
        z, x, y = mbtiles.center_tile()
        return tile(request, name, z, x, y)
    except MBTilesNotFoundError, e:
        logger.warning(e)
    raise Http404


def grid(request, name, z, x, y, catalog=None):
    """ Serve a single UTF-Grid tile """
    callback = request.GET.get('callback', None)
    try:
        mbtiles = MBTiles(name, catalog)
        return HttpResponse(
            mbtiles.grid(z, x, y, callback),
            content_type = 'application/javascript; charset=utf8'
        )
    except MBTilesNotFoundError, e:
        logger.warning(e)
    except MissingTileError:
        logger.warning(_("Grid tile %s not available in %s") % ((z, x, y), name))
    raise Http404


def tilejson(request, name, catalog=None):
    """ Serve the map configuration as TileJSON """
    callback = request.GET.get('callback', None)
    try:
        mbtiles = MBTiles(name, catalog)
        tilejson = mbtiles.tilejson(request)
        if callback:
            tilejson = '%s(%s);' % (callback, tilejson)
        return HttpResponse(tilejson,
                            content_type='application/javascript; charset=utf8')
    except MBTilesNotFoundError, e:
        logger.warning(e)
    raise Http404
