import sys, math, urllib.request, io, operator
from tile_system import *
from PIL import Image

def getURL(quadkey):
        license_key = "Aq3bmbTehDPHWHjRsSsw1oKi3z5bYUewA4t0LQp09ZU8HbVvXbW2HXRiFwshMf8h"
        return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&key=%s" % (quadkey, license_key)

def getImageFromQuadkey(quadkey):
        socket = urllib.request.urlopen(getURL(quadkey))
        tinker = socket.read()
        img = Image.open(io.BytesIO(tinker))
        print('loading tiles....')
        return img

def getLowestQuality(lat1, lon1, lat2, lon2):
        '''
        Here we search for the lowest Level of Detail that contains minimum number of tiles.
        '''
        i = 1
        for i in range(23, 0, -1):
                tx1, ty1 = LatLongToTileXY(lat1, lon1, i)
                tx2, ty2 = LatLongToTileXY(lat2, lon2, i)
                if tx1 > tx2:
                        tx1, tx2 = tx2, tx1
                if ty1 > ty2:
                        ty1, ty2 = ty2, ty1
                if (tx2 - tx1 <= 1) and (ty2 - ty1 <= 1):
                        print ("Lowest Quality found at "),
                        print (i)
                        return i, tx1, ty1

        
def main():
        try:
                
                lat1 = float(sys.argv[1])
                lon1 = float(sys.argv[2])
                lat2 = float(sys.argv[3])
                lon2 = float(sys.argv[4])
        except:
                print('You did not input any position.')
                print('Now using default setting')
                lat1 = float(12)
                lon1 = float(12)
                lat2 = float(13)
                lon2 = float(13)
        
        framework = 8192
        ministemp = 64
        blank = Image.new('RGB', (framework, framework))

        quality, tx, ty = getLowestQuality(lat1, lon1, lat2, lon2)
        tx0=tx
        ty0=ty
        curr_tile_size = int(framework/2)
        flag = True
        q=quality
        # we use a while loop and refresh the whole image for lowest quality to the best we can get. and pass the recent base quality image to best
        best_quality = blank
        while q <= 23 and curr_tile_size >= ministemp and flag:

                print ("Current level of detials ",)
                print (q)
                print ("curr_tile_size is",)
                print (curr_tile_size)
                tx1, ty1 = LatLongToTileXY(lat1, lon1, q)
                tx2, ty2 = LatLongToTileXY(lat2, lon2, q)
                if tx1 > tx2:
                        tx1, tx2 = tx2, tx1
                if ty1 > ty2:
                        ty1, ty2 = ty2, ty1
                for x in range(tx1, tx2+1):
                        if not flag:
                                break
                        for y in range(ty1, ty2+1):
                                if not flag:
                                        break
                                curr_quadKey = TileXYToQuadKey(x, y, q)
                                print ("curr_quadKey is",)
                                print (curr_quadKey)

                                try:
                                #if flag:
                                        curr_image = getImageFromQuadkey(curr_quadKey)

                                        if not curr_image == Image.open('null.jpeg'):
                                                curr_image = curr_image.resize((curr_tile_size, curr_tile_size))
                                                start_x = (x - tx0) * curr_tile_size 
                                                start_y = (y - ty0) * curr_tile_size
                                                end_x = start_x + curr_tile_size
                                                end_y = start_y + curr_tile_size
                                                blank.paste(curr_image, (start_x, start_y, end_x, end_y))
                                        else:
                                                flag = False
                                                print('No content for this QuadKey')
                                                break
                                #else:
                                except:
                                        print('time out in connecting to server or cannot find more detailed image')
                                        flag =False
                                        break


                tx0 = tx0 * 2
                ty0 = ty0 * 2
                q += 1
                curr_tile_size= int(curr_tile_size/2)
                if flag:
                        best_quality = blank
        print ("Refinary is finished")
        px1,py1=LatLongToPixelXY(lat1, lon1, quality)
        px2,py2=LatLongToPixelXY(lat2, lon2, quality)
        print(px1,py1)
        print(px2,py2)
        px1d=(framework/512)*(px1 -tx*256)
        py1d=(framework/512)*(py1 -ty*256)
        px2d=(framework/512)*(px2 -tx*256)
        py2d=(framework/512)*(py2 -ty*256)
        print(px1d,py1d)
        print(px2d,py2d)
        raw = best_quality.load()
        edge=int(framework/1024)
        for aa in range(framework-1):
                for bb in range(framework-1):
                        if abs(aa-px1d)<edge or abs(aa-px2d)<edge or abs(bb-py1d)<edge or abs(bb-py2d)<edge:
                                raw[aa,bb]=(250,250,250)
                        
        print ("windowing finished")
        best_quality.save('complete.jpeg')


        

if __name__ == '__main__':
        main()

#test beijing python main.py 39.922972  116.391452  39.913413  116.402439
#test copenhagen python main.py 55.694191  12.590022  55.688470  12.598863

#http://h0.ortho.tiles.virtualearth.net/tiles/h132100103322230.jpeg?g=131&key=Aq3bmbTehDPHWHjRsSsw1oKi3z5bYUewA4t0LQp09ZU8HbVvXbW2HXRiFwshMf8h
