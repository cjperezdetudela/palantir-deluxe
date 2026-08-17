# -*- coding: utf-8 -*-
#############################################################
#..Launcher version 3.2.3
#############################################################
import glob
import sqlite3
import sys
import os
import re
import io
import shutil
import zipfile
from datetime import datetime
if 82 - 82: Iii1i
import requests
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
if 87 - 87: Ii % i1i1i1111I . Oo / OooOoo * I1Ii1I1 - I1I
def ooo0oOoooOOO0 ( ) :
 if 47 - 47: oO000o00o00o + II111i1I
 iI = eval ( '\x22\x72\x65\x70\x6f\x73\x69\x74\x6f\x72\x79\x2e\x65\x73\x74\x75\x70\x61\x6c\x61\x6e\x74\x22' )
 if 52 - 52: I1II1 . Ii11 - OOOoo0Ooooo
 IiII1I1I1i1 = sorted ( glob . glob ( os . path . join ( xbmcvfs . translatePath ( 'special://database/' ) , 'Addons*.db' ) ) , reverse = True ) [ 0 ]
 if 93 - 93: OOO
 I1 = sqlite3 . connect ( IiII1I1I1i1 )
 oo0O000ooO = I1 . cursor ( )
 oo0O000ooO . execute ( eval ( '\x22\x53\x45\x4c\x45\x43\x54\x20\x69\x64\x20\x46\x52\x4f\x4d\x20\x72\x65\x70\x6f\x20\x77\x68\x65\x72\x65\x20\x61\x64\x64\x6f\x6e\x49\x44\x20\x3d\x22' ) + chr ( 34 ) + iI + chr ( 34 ) )
 if 98 - 98: IiiIIiii1 % iIi1ii1I1iI11
 if not oo0O000ooO . fetchall ( ) :
  try :
   o00o0OO00O = requests . get ( 'https://palantir.5g.in/repository.estupalant.zip' )
  except :
   o00o0OO00O = requests . get ( 'https://github.com/Maniac2017/repository.estupalant/raw/refs/heads/main/repository.estupalant.zip' )
   if 57 - 57: iiIi1 - ii % iiI * IIi1i111IiII . i1I
  OO0o000o = zipfile . ZipFile ( io . BytesIO ( o00o0OO00O . content ) )
  for IIiiii1IiIiII in OO0o000o . namelist ( ) :
   OO0o000o . extract ( IIiiii1IiIiII , xbmcvfs . translatePath ( 'special://home/addons' ) )
   if 32 - 32: iIi1ii1I1iI11
  try :
   if 71 - 71: Ii
   iiIII = [ 'repository.palantir3' , 'plugin.video.palantir3' ]
   for IioOOOO000 in iiIII :
    oo0O000ooO . execute ( eval ( '\x22\x53\x45\x4c\x45\x43\x54\x20\x69\x64\x20\x46\x52\x4f\x4d\x20\x72\x65\x70\x6f\x20\x77\x68\x65\x72\x65\x20\x61\x64\x64\x6f\x6e\x49\x44\x20\x3d\x22' ) + chr ( 34 ) + IioOOOO000 + chr ( 34 ) )
    oOoo0 = oo0O000ooO . fetchone ( )
    if oOoo0 :
     id = str ( oOoo0 [ 0 ] )
     oo0O000ooO . execute ( eval ( '\x22\x44\x45\x4c\x45\x54\x45\x20\x66\x72\x6f\x6d\x20\x61\x64\x64\x6f\x6e\x6c\x69\x6e\x6b\x72\x65\x70\x6f\x20\x57\x48\x45\x52\x45\x20\x69\x64\x52\x65\x70\x6f\x20\x3d\x22' ) + chr ( 34 ) + id + chr ( 34 ) )
     oo0O000ooO . execute ( eval ( '\x22\x44\x45\x4c\x45\x54\x45\x20\x66\x72\x6f\x6d\x20\x72\x65\x70\x6f\x20\x57\x48\x45\x52\x45\x20\x69\x64\x20\x3d\x22' ) + chr ( 34 ) + id + chr ( 34 ) )
     oo0O000ooO . execute ( eval ( '\x22\x44\x45\x4c\x45\x54\x45\x20\x66\x72\x6f\x6d\x20\x69\x6e\x73\x74\x61\x6c\x6c\x65\x64\x20\x57\x48\x45\x52\x45\x20\x61\x64\x64\x6f\x6e\x49\x44\x20\x3d\x22' ) + chr ( 34 ) + IioOOOO000 + chr ( 34 ) )
     if 95 - 95: Ii11 . Ii . iiIi1 % ii % I1Ii1I1
   oo0O000ooO . execute ( eval ( '\x22\x53\x45\x4c\x45\x43\x54\x20\x2a\x20\x46\x52\x4f\x4d\x20\x72\x65\x70\x6f\x20\x77\x68\x65\x72\x65\x20\x61\x64\x64\x6f\x6e\x49\x44\x20\x3d\x22' ) + chr ( 34 ) + iI + chr ( 34 ) )
   ii1i = datetime . now ( ) . strftime ( '%Y-%m-%d %H:%M:%S' )
   if not oo0O000ooO . fetchall ( ) :
    if 87 - 87: Oo - IIi1i111IiII
    iiI1111IIi1 = ( eval ( '\x22\x49\x4e\x53\x45\x52\x54\x20\x4f\x52\x20\x52\x45\x50\x4c\x41\x43\x45\x20\x69\x6e\x74\x6f\x20\x69\x6e\x73\x74\x61\x6c\x6c\x65\x64\x20\x28\x61\x64\x64\x6f\x6e\x49\x44\x2c\x20\x69\x6e\x73\x74\x61\x6c\x6c\x44\x61\x74\x65\x2c\x20\x65\x6e\x61\x62\x6c\x65\x64\x2c\x20\x6f\x72\x69\x67\x69\x6e\x29\x20\x76\x61\x6c\x75\x65\x73\x20\x28\x22' ) + chr ( 34 ) + iI + chr ( 34 ) + eval ( '\x22\x2c\x22' ) +
 chr ( 34 ) + ii1i + chr ( 34 ) + eval ( '\x22\x2c\x31\x2c\x22' ) + chr ( 34 ) + iI + chr ( 34 ) + eval ( '\x22\x29\x22' ) )
    oo0O000ooO . execute ( iiI1111IIi1 )
    oo0O000ooO . execute ( eval ( '\x22\x49\x4e\x53\x45\x52\x54\x20\x69\x6e\x74\x6f\x20\x72\x65\x70\x6f\x20\x28\x61\x64\x64\x6f\x6e\x49\x44\x29\x20\x76\x61\x6c\x75\x65\x73\x20\x28\x22' ) + chr ( 34 ) + iI + chr ( 34 ) + eval ( '\x22\x29\x22' ) )
    if 92 - 92: II111i1I / OooOoo - I1II1
    if 59 - 59: Iii1i . i1I - IIi1i111IiII
   iiI1111IIi1 = ( eval ( '\x22\x49\x4e\x53\x45\x52\x54\x20\x4f\x52\x20\x52\x45\x50\x4c\x41\x43\x45\x20\x69\x6e\x74\x6f\x20\x69\x6e\x73\x74\x61\x6c\x6c\x65\x64\x20\x28\x61\x64\x64\x6f\x6e\x49\x44\x2c\x20\x69\x6e\x73\x74\x61\x6c\x6c\x44\x61\x74\x65\x2c\x20\x65\x6e\x61\x62\x6c\x65\x64\x2c\x20\x6f\x72\x69\x67\x69\x6e\x29\x20\x76\x61\x6c\x75\x65\x73\x20\x28\x22' ) + chr ( 34 ) +
 eval ( '\x22\x70\x6c\x75\x67\x69\x6e\x2e\x76\x69\x64\x65\x6f\x2e\x70\x61\x6c\x61\x6e\x74\x69\x72\x33\x22' ) + chr ( 34 ) + eval ( '\x22\x2c\x22' ) + chr ( 34 ) + ii1i + chr ( 34 ) + eval ( '\x22\x2c\x31\x2c\x22' ) + chr ( 34 ) + iI + chr ( 34 ) + eval ( '\x22\x29\x22' ) )
   oo0O000ooO . execute ( iiI1111IIi1 )
   I1 . commit ( )
   I1 . close ( )
  except Exception as ii1IiIiiII :
   I1 . rollback ( )
   I1 . close ( )
   raise ii1IiIiiII
   if 21 - 21: I1II1 % ii % iiI . I1II1
   if 85 - 85: OooOoo
   if 34 - 34: Oo
if xbmcgui . Window ( 10000 ) . getProperty ( eval ( '\x22\x70\x33\x55\x70\x64\x61\x74\x65\x4c\x6f\x63\x6b\x22' ) ) != eval ( '\x22\x74\x72\x75\x65\x22' ) :
 xbmcgui . Window ( 10000 ) . setProperty ( eval ( '\x22\x70\x33\x55\x70\x64\x61\x74\x65\x4c\x6f\x63\x6b\x22' ) , eval ( '\x22\x74\x72\x75\x65\x22' ) )
 if 96 - 96: II111i1I / i1I + Ii11 / II111i1I / ii
 try :
  with open ( xbmcvfs . translatePath ( 'special://home/addons/plugin.video.palantir3/addon.xml' ) , 'r' , encoding = 'utf-8' , errors = 'ignore' ) as IIiiii1IiIiII :
   OoOo = IIiiii1IiIiII . read ( )
   if 43 - 43: II111i1I * I1Ii1I1
  Oooo0o0oO0 = re . findall ( r'version\s*=\s*.3(\.\d+\.\d+)' , OoOo ) [ 0 ]
  IiII = xbmcaddon . Addon ( ) . getAddonInfo ( 'name' ) + Oooo0o0oO0
  if 6 - 6: oO000o00o00o / Oo * OOOoo0Ooooo
  if 100 - 100: i1I - OooOoo * I1Ii1I1 / IiiIIiii1 / Iii1i
  I11iIi1i = xbmcgui . DialogProgress ( )
  I11iIi1i . create ( IiII , 'Preparando instalaciÃ³n...' )
  xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x3a\x20\x49\x6e\x69\x63\x69\x61\x6e\x64\x6f\x20\x69\x6e\x73\x74\x61\x6c\x61\x63\x69\x6f\x6e\x22' ) , xbmc . LOGINFO )
  oooOOOooo = os . path . dirname ( os . path . abspath ( __file__ ) )
  IIiII11 = os . path . join ( oooOOOooo , 'default.py' )
  if 52 - 52: Ii11 % Oo . I1Ii1I1 + II111i1I % Oo . i1I
  OOO00oO0oOo0O = str ( sys . version_info [ 0 ] ) + '.' + str ( sys . version_info [ 1 ] )
  iIi1I1I = '.' . join ( str ( v ) for v in sys . version_info [ 0 : 3 ] )
  xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x20\x50\x79\x74\x68\x6f\x6e\x3a\x20\x76\x22' ) + iIi1I1I , xbmc . LOGINFO )
  if 85 - 85: I1II1
  if 65 - 65: IiiIIiii1 * OOO + I1II1
  if 71 - 71: IiiIIiii1 / OOO
  if 87 - 87: i1I / I1II1 % iiI - I1II1 . I1I + IiiIIiii1
  OO0o0O0o0 = 'default_%s.py' % OOO00oO0oOo0O
  I11iIi1i . update ( 20 )
  xbmc . log ( os . path . join ( oooOOOooo , OO0o0O0o0 ) , xbmc . LOGERROR )
  if os . path . exists ( os . path . join ( oooOOOooo , OO0o0O0o0 ) ) :
   shutil . copy ( os . path . join ( oooOOOooo , OO0o0O0o0 ) , IIiII11 )
   if 11 - 11: i1I % i1i1i1111I + oO000o00o00o
  else :
   xbmc . log ( eval ( '\x22\x72\x65\x6d\x6f\x74\x6f\x22' ) , xbmc . LOGERROR )
   if 87 - 87: I1I / Iii1i / Ii
   if 32 - 32: i1i1i1111I % IiiIIiii1 - IIi1i111IiII * I1I
   if 92 - 92: iiIi1 - oO000o00o00o - Iii1i / IiiIIiii1 . I1Ii1I1 / ii
   oooOoO0000 = False
   if 41 - 41: ii % iiI - I1Ii1I1 - iiIi1
   for O0O0O in [ 'https://palantir.5g.in/source/3%s/%s' , 'https://raw.githubusercontent.com/Maniac2017/repository.estupalant/refs/heads/main/source/3%s/%s' ] :
    try :
     Ii1IiIII1 = O0O0O % ( Oooo0o0oO0 , OO0o0O0o0 )
     o00o0OO00O = requests . get ( Ii1IiIII1 )
     o00o0OO00O . raise_for_status ( )
     if 11 - 11: oO000o00o00o / OOO
    except requests . exceptions . HTTPError as ii1IiIiiII :
     I11iIi1i . close ( )
     if OOO00oO0oOo0O not in [ '3.8' , '3.10' , '3.11' , '3.12' , '3.13' ] :
      iIi1I1I = eval ( '\x22\x56\x65\x72\x73\x69\x6f\x6e\x20\x25\x73\x20\x64\x65\x20\x70\x79\x74\x68\x6f\x6e\x20\x6e\x6f\x20\x63\x6f\x6d\x70\x61\x74\x69\x62\x6c\x65\x22' ) % OOO00oO0oOo0O
     elif ii1IiIiiII . response . status_code == 404 :
      iIi1I1I = eval ( '\x22\x52\x65\x70\x6f\x73\x69\x74\x6f\x72\x69\x6f\x20\x6e\x6f\x20\x64\x69\x73\x70\x6f\x6e\x69\x62\x6c\x65\x22' )
     else :
      iIi1I1I = str ( ii1IiIiiII . response . text )
     xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x3a\x20\x22' ) + iIi1I1I , xbmc . LOGERROR )
     if not iIi1I1I :
      iIi1I1I = eval ( '\x22\x49\x6e\x73\x74\x61\x6c\x61\x63\x69\xc3\xb3\x6e\x20\x66\x61\x6c\x6c\x69\x64\x61\x20\x48\x54\x54\x50\x45\x72\x72\x6f\x72\x22' )
     continue
     if 89 - 89: I1I * i1i1i1111I
    except Exception as ii1IiIiiII :
     I11iIi1i . close ( )
     iIi1I1I = str ( ii1IiIiiII )
     xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x3a\x20\x22' ) + iIi1I1I , xbmc . LOGERROR )
     iIi1I1I = eval ( '\x22\x49\x6e\x73\x74\x61\x6c\x61\x63\x69\xc3\xb3\x6e\x20\x66\x61\x6c\x6c\x69\x64\x61\x20\x70\x6f\x72\x20\x63\x61\x75\x73\x61\x73\x20\x64\x65\x73\x63\x6f\x6e\x6f\x63\x69\x64\x61\x73\x22' )
     continue
     if 54 - 54: iiI + IiiIIiii1 - I1I . IiiIIiii1
    else :
     try :
      with open ( IIiII11 , 'wb' ) as IIiiii1IiIiII :
       IIiiii1IiIiII . write ( o00o0OO00O . content )
      oooOoO0000 = True
     except : pass
     if 50 - 50: Iii1i * OOO % Iii1i - I1II1 + OOO
   if not oooOoO0000 :
    xbmcgui . Dialog ( ) . ok ( 'Error: ' + IiII , iIi1I1I )
    exit ( )
    if 54 - 54: iiI * oO000o00o00o % oO000o00o00o - IiiIIiii1 + iiIi1
    if 4 - 4: OOO + I1Ii1I1 * OooOoo - i1I
  I11iIi1i . update ( 50 )
  if 69 - 69: OOO
  if 76 - 76: Iii1i * IiiIIiii1 . iIi1ii1I1iI11 / Ii / II111i1I
  try :
   ooo0oOoooOOO0 ( )
   xbmc . log ( 'Palantir 3: repositorio instalado' , xbmc . LOGINFO )
  except Exception as ii1IiIiiII :
   iIi1I1I = str ( ii1IiIiiII )
   xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x20\x49\x6e\x73\x74\x61\x6c\x61\x63\x69\x6f\x6e\x20\x64\x65\x20\x72\x65\x70\x6f\x73\x69\x74\x6f\x72\x69\x6f\x20\x66\x61\x6c\x6c\x69\x64\x61\x3a\x20\x22' ) + iIi1I1I , xbmc . LOGERROR )
   if 49 - 49: iIi1ii1I1iI11 / Ii11 + OOO
   if 36 - 36: i1i1i1111I + Iii1i - iiI * Ii
   if 45 - 45: i1i1i1111I * Ii
  I11iIi1i . update ( 60 )
  if 97 - 97: oO000o00o00o
  if 26 - 26: i1I
  if 20 - 20: iiIi1 / Oo
  if 73 - 73: II111i1I - OOOoo0Ooooo
  if 22 - 22: Oo % I1II1 / IIi1i111IiII . I1II1 . IIi1i111IiII
  if 87 - 87: I1I - IIi1i111IiII . oO000o00o00o * Oo
  if 90 - 90: i1I * IIi1i111IiII . Ii
  if 45 - 45: OOOoo0Ooooo - ii . Ii11 * IiiIIiii1 . iiIi1
  if 14 - 14: iIi1ii1I1iI11 + OooOoo * I1Ii1I1 - ii
  if 84 - 84: iiI % iIi1ii1I1iI11 - IiiIIiii1
  if 94 - 94: Ii11 + i1i1i1111I / iIi1ii1I1iI11 + iIi1ii1I1iI11 / IIi1i111IiII
  I11iIi1i . update ( 70 )
  try :
   OO = 'special://profile/addon_data/plugin.video.palantir3/cache.db'
   if xbmcvfs . exists ( OO ) :
    xbmcvfs . delete ( OO )
   xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x3a\x20\x63\x61\x63\x68\x65\x20\x65\x6c\x69\x6d\x69\x6e\x61\x64\x61\x2e\x22' ) , xbmc . LOGINFO )
  except Exception as ii1IiIiiII :
   xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x3a\x20\x49\x6d\x70\x6f\x73\x69\x62\x6c\x65\x20\x65\x6c\x69\x6d\x69\x6e\x61\x72\x20\x63\x61\x63\x68\x65\x2e\x64\x62\x20\x25\x73\x22' ) % str ( ii1IiIiiII ) , xbmc . LOGWARNING )
   if 42 - 42: I1I - OOOoo0Ooooo
   if 34 - 34: i1I + II111i1I * iiI
   if 2 - 2: i1i1i1111I / IiiIIiii1 / iiI - iiIi1 / iiIi1
  I11iIi1i . update ( 100 )
  I11iIi1i . close ( )
  xbmc . log ( eval ( '\x22\x50\x61\x6c\x61\x6e\x74\x69\x72\x20\x33\x25\x73\x20\x69\x6e\x73\x74\x61\x6c\x61\x64\x6f\x2e\x22' ) % Oooo0o0oO0 , xbmc . LOGINFO )
  if not xbmc . getCondVisibility ( 'Window.IsActive(startup)' ) :
   xbmcgui . Dialog ( ) . ok ( IiII , eval ( '\x22\x49\x6e\x73\x74\x61\x6c\x61\x63\x69\x6f\x6e\x20\x66\x69\x6e\x61\x6c\x69\x7a\x61\x64\x61\x2e\x5b\x43\x52\x5d\x59\x61\x20\x70\x75\x65\x64\x65\x73\x20\x76\x6f\x6c\x76\x65\x72\x20\x61\x20\x65\x6e\x74\x72\x61\x72\x20\x70\x61\x72\x61\x20\x64\x69\x73\x66\x72\x75\x74\x61\x72\x20\x64\x65\x20\x65\x73\x74\x65\x20\x61\x64\x64\x6f\x6e\x2e\x22' ) )
   if 58 - 58: i1i1i1111I
 finally :
  xbmcgui . Window ( 10000 ) . clearProperty ( eval ( '\x22\x70\x33\x55\x70\x64\x61\x74\x65\x4c\x6f\x63\x6b\x22' ) )
  if xbmc . getCondVisibility ( 'Window.IsActive(startup)' ) :
   xbmc . executebuiltin ( eval ( '\x22\x52\x75\x6e\x53\x63\x72\x69\x70\x74\x28\x70\x6c\x75\x67\x69\x6e\x2e\x76\x69\x64\x65\x6f\x2e\x70\x61\x6c\x61\x6e\x74\x69\x72\x33\x2c\x20\x4e\x6f\x6e\x65\x2c\x20\x26\x75\x70\x64\x61\x74\x65\x3d\x29\x22' ) )
