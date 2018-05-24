bl_info = {
    "name": "RhinOnBlender",
    "author": "Cicero Moraes, Pablo Maricevich, Rodrigo Dornelles e Everton da Rosa",
    "version": (1, 0, 2),
    "blender": (2, 75, 0),
    "location": "View3D",
    "description": "Planejamento de Rinoplastia no Blender",
    "warning": "",
    "wiki_url": "",
    "category": "rhin",
    }

import bpy
import bmesh
from math import sqrt
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
import tempfile
import subprocess
import math
from os.path import expanduser
import platform
import shutil


def RhinGeraModeloFotoDef(self, context):
    scn = context.scene

    tmpdir = tempfile.gettempdir()

    homeall = expanduser("~")

    try:

        OpenMVGtmpDir = tmpdir + '/OpenMVG'
        tmpOBJface = tmpdir + '/MVS/scene_dense_mesh_texture2.obj'

        if platform.system() == "Linux":
            OpenMVGPath = homeall + '/Programs/OrtogOnBlender/openMVG/software/SfM/SfM_SequentialPipeline.py'
            OpenMVSPath = homeall + '/Programs/OrtogOnBlender/openMVS/OpenMVSrhin.sh'

        if platform.system() == "Windows":
            OpenMVGPath = 'C:/OrtogOnBlender/openMVGWin/software/SfM/SfM_SequentialPipeline.py'
            OpenMVSPath = 'C:/OrtogOnBlender/openMVSWin/OpenMVSrhin.bat'

        if platform.system() == "Darwin":
            OpenMVGPath = homeall + '/OrtogOnBlender/openMVGMACelcap/SfM_SequentialPipeline.py'
            OpenMVSPath = homeall + '/OrtogOnBlender/openMVSMACelcap/OpenMVSrhinMAC.sh'

        shutil.rmtree(tmpdir + '/OpenMVG', ignore_errors=True)
        shutil.rmtree(tmpdir + '/MVS', ignore_errors=True)

        if platform.system() == "Linux":
            subprocess.call(['python', OpenMVGPath, scn.my_tool.path, OpenMVGtmpDir])

        if platform.system() == "Windows":
            subprocess.call(['C:/OrtogOnBlender/Python27/python', OpenMVGPath, scn.my_tool.path, OpenMVGtmpDir])

        if platform.system() == "Darwin":
            subprocess.call(['python', OpenMVGPath, scn.my_tool.path, OpenMVGtmpDir])

        subprocess.call(OpenMVSPath, shell=True)

        #    subprocess.call([ 'meshlabserver', '-i', tmpdir+'scene_dense_mesh_texture.ply', '-o', tmpdir+'scene_dense_mesh_texture2.obj', '-om', 'vn', 'wt' ])

        bpy.ops.import_scene.obj(filepath=tmpOBJface, filter_glob="*.obj;*.mtl")

        scene_dense_mesh_texture2 = bpy.data.objects['scene_dense_mesh_texture2']

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = scene_dense_mesh_texture2
        bpy.data.objects['scene_dense_mesh_texture2'].select = True

        bpy.context.object.data.use_auto_smooth = False
        bpy.context.object.active_material.specular_hardness = 60
        bpy.context.object.active_material.diffuse_intensity = 0.6
        bpy.context.object.active_material.specular_intensity = 0.3
        bpy.context.object.active_material.specular_color = (0.233015, 0.233015, 0.233015)

        bpy.ops.object.modifier_add(type='SMOOTH')
        bpy.context.object.modifiers["Smooth"].factor = 2
        bpy.context.object.modifiers["Smooth"].iterations = 3
        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        bpy.ops.view3d.view_all(center=False)
        bpy.ops.file.pack_all()

        # Displacement

        context = bpy.context
        obj = context.active_object

        heightTex = bpy.data.textures.new('Texture name', type='IMAGE')
        heightTex.image = bpy.data.images['scene_dense_mesh_texture2_material_0_map_Kd.jpg']
        dispMod = obj.modifiers.new("Displace", type='DISPLACE')
        dispMod.texture = heightTex
        bpy.context.object.modifiers["Displace"].texture_coords = 'UV'
        bpy.context.object.modifiers["Displace"].strength = 0.035
        bpy.context.object.modifiers["Displace"].mid_level = 0.5

        bpy.ops.object.shade_smooth()


    #       bpy.ops.object.convert(target='MESH')

    except RuntimeError:
        bpy.context.window_manager.popup_menu(ERROruntimeFotosDef, title="Atenção!", icon='INFO')


class RhinGeraModeloFoto(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.rhin_gera_modelo_foto"
    bl_label = "Gera Modelos Foto"

    def execute(self, context):
        RhinGeraModeloFotoDef(self, context)
        return {'FINISHED'}

def RhinImportaMedNarizDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene
    
    dirScript = bpy.utils.user_resource('SCRIPTS')

    blendfile = dirScript+"addons/RhinOnBlender-master/objetos.blend"
    section   = "\\Group\\"
    object    = "MedidasNariz"

    filepath  = blendfile + section + object
    directory = blendfile + section
    filename  = object

    bpy.ops.wm.append(
        filepath=filepath, 
        filename=filename,
        directory=directory)
        
class RhinImportaMedNariz(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.rhin_importa_med_nariz"
    bl_label = "Importa Medidas Nariz"
    
    def execute(self, context):
        RhinImportaMedNarizDef(self, context)
        return {'FINISHED'}

# CRIA PLANO SECÇÃO

def RhinCriaPlanoSeccaoDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.ops.mesh.primitive_plane_add()
    bpy.context.object.name = "PlanoSeccaoPrePos"
    bpy.ops.transform.resize(value=(150, 150, 150))
    bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0))
    


class RhinCriaPlanoSeccao(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.rhin_plano_seccao"
    bl_label = "Cria Plano de Secção"
    
    def execute(self, context):
        RhinCriaPlanoSeccaoDef(self, context)
        return {'FINISHED'}

# MOSTRA/OCULTA FACE

def RhinMostraOcultaFaceDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.data.objects["face_copia"].hide = not bpy.data.objects["face_copia"].hide


class RhinMostraOcultaFace(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.mostra_oculta_face"
    bl_label = "Mostra Oculta Face"
    
    def execute(self, context):
        RhinMostraOcultaFaceDef(self, context)
        return {'FINISHED'}

# PIVO CURSOR

def RhinPivoCursorDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.context.space_data.pivot_point = 'CURSOR'

class RhinPivoCursor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.pivo_cursor"
    bl_label = "Pivô Cursor"
    
    def execute(self, context):
        RhinPivoCursorDef(self, context)
        return {'FINISHED'}


# CRIA ESPESSURA GUIA

def RhinCriaEspessuraDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.ops.object.modifier_add(type='SOLIDIFY') 
    bpy.context.object.modifiers["Solidify"].thickness = 4
    bpy.context.object.modifiers["Solidify"].offset = 1

class RhinCriaEspessura(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.cria_espessura"
    bl_label = "Cria Espessura"
    
    def execute(self, context):
        RhinCriaEspessuraDef(self, context)
        return {'FINISHED'}

# ESCULTURA GRAB

def RhinEsculturaGrabDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    bpy.ops.paint.brush_select(paint_mode='SCULPT', sculpt_tool='GRAB')
    bpy.ops.brush.curve_preset(shape='ROOT')

class RhinEsculturaGrab(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.escultura_grab"
    bl_label = "Escultura Grab"
    
    def execute(self, context):
        RhinEsculturaGrabDef(self, context)
        return {'FINISHED'}

# CRIA COPIA ROSTO

def RhinRostoCriaCopiaDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene
    
    obj.name="face"

    bpy.ops.object.duplicate()
  
    obj2 = context.active_object
 
    obj2.name="face_copia"
    obj2.hide = True


class RhinRostoCriaCopia(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.rosto_cria_copia"
    bl_label = "Rosto Cria Copia"
    
    def execute(self, context):
        RhinRostoCriaCopiaDef(self, context)
        return {'FINISHED'}

# RNDERIZAÇÕES PRÉ E PÓS

def RhinRenderPrePosDef(self, context):

    context = bpy.context
    obj = context.active_object
    scn = context.scene

    tmpdir = tempfile.gettempdir()
    tmpImgPos = tmpdir+"/ImgPos.png"
    tmpImgPre = tmpdir+"/ImgPre.png"
    tmpImgPrePos = tmpdir+"/ImgPrePos.png"
    
    
    face = bpy.data.objects['face']
    face_copia = bpy.data.objects['face_copia']
    
    # Gera imagem do pós

    bpy.ops.object.select_all(action='DESELECT')
    face.select = True
    bpy.context.scene.objects.active = face
    bpy.ops.object.select_all(action='INVERT') # inverte seleção
    bpy.ops.object.hide_view_set(unselected=False) # deixe seleção insivível
    bpy.ops.render.opengl()    
    bpy.data.images['Render Result'].save_render( tmpImgPos ) 
    bpy.ops.object.hide_view_clear() # tudo visível
    
    # Gera imagem do pré

    bpy.ops.object.select_all(action='DESELECT')
    face_copia.select = True
    bpy.context.scene.objects.active = face_copia
    bpy.ops.object.select_all(action='INVERT')
    bpy.ops.object.hide_view_set(unselected=False)
    bpy.ops.render.opengl()    
    bpy.data.images['Render Result'].save_render( tmpImgPre ) 
    bpy.ops.object.hide_view_clear()

    subprocess.call(['composite', '-blend', '50', '-gravity', 'South', tmpImgPre, tmpImgPos, '-alpha', 'Set', tmpImgPrePos])
 
    bpy.ops.image.open(filepath="tmpImgPrePos", directory=tmpdir, files=[{"name":"ImgPrePos.png", "name":"ImgPrePos.png"}], relative_path=True, show_multiview=False)
    imagePrePosImgEd = bpy.data.images['ImgPrePos.png']
    bpy.data.screens['UV Editing'].areas[1].spaces[0].image = imagePrePosImgEd
    
    bpy.ops.image.open(filepath="tmpImgPre", directory=tmpdir, files=[{"name":"ImgPre.png", "name":"ImgPre.png"}], relative_path=True, show_multiview=False)
    imagePreImgEd = bpy.data.images['ImgPre.png']
    bpy.data.screens['UV Editing'].areas[1].spaces[0].image = imagePreImgEd
    
    bpy.ops.image.open(filepath="tmpImgPos", directory=tmpdir, files=[{"name":"ImgPos.png", "name":"ImgPos.png"}], relative_path=True, show_multiview=False)
    imagePosImgEd = bpy.data.images['ImgPos.png']
    bpy.data.screens['UV Editing'].areas[1].spaces[0].image = imagePosImgEd
    
class RhinRenderPrePos(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "render.render_pre_pos"
    bl_label = "Importa estrutura de bones"
    
    def execute(self, context):
        RhinRenderPrePosDef(self, context)
        return {'FINISHED'}


# DISTANCIA OBJETOS    

def RhinDistanciaObjetosDef(self, context):
    """
    return: float. Distance of the two objects
    Must select two objects
    """
    l = []
    CimaMeio = [bpy.data.objects['MarcaMeio'], bpy.data.objects['MarcaTopo']]
    
    for item in CimaMeio:
       l.append(item.location)

    distanciaMaior = sqrt( (l[0][0] - l[1][0])**2 + (l[0][1] - l[1][1])**2 + (l[0][2] - l[1][2])**2)
    print(distanciaMaior)  # print distance to console, DEBUG

    l2 = []
    MeioBaixo = [bpy.data.objects['MarcaMeio'], bpy.data.objects['MarcaBaixo']]

    for item in MeioBaixo:
       l2.append(item.location)

    distanciaMenor = sqrt( (l2[0][0] - l2[1][0])**2 + (l2[0][1] - l2[1][1])**2 + (l2[0][2] - l2[1][2])**2)
    print(distanciaMenor)  # print distance to console, DEBUG

    Fator = distanciaMenor / distanciaMaior
    print(Fator)
    
    bpy.data.objects["TextFator"].data.body = str(int(Fator)+float(str(Fator-int(Fator))[1:4]))
    
    Anl = bpy.data.objects['Empty_Na_Atras']
    Bnl = bpy.data.objects['Empty_Na_Frente']

    AnlBnl = math.sqrt( (Anl.location[1] - Bnl.location[1])**2 + (Anl.location[2] - Bnl.location[2])**2 )

    BnlCnl = math.sqrt( (Bnl.location[1] - Bnl.location[1])**2 + (Bnl.location[2] - Anl.location[2])**2 )

    valorAng = BnlCnl / AnlBnl

    angNasolabial = (math.asin(valorAng)*180/math.pi)+90


    bpy.data.objects["TextNasolabial"].data.body = str(int(angNasolabial)+float(str(angNasolabial-int(angNasolabial))[1:4]))+'º'

    return Fator

#get_distance()

class RhinDistanciaObjetos(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.distancia_objetos"
    bl_label = "Distância Objetos"
    
    def execute(self, context):
        RhinDistanciaObjetosDef(self, context)
        return {'FINISHED'}


# ZOOM
class RhinZoomCena(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Zoom Cena"
    bl_idname = "rhin_zoom_cena"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.operator("view3d.viewnumpad", text="Frente").type='FRONT'
        row.operator("view3d.viewnumpad", text="Atrás").type='BACK'
        
        row = layout.row()
        row.operator("view3d.viewnumpad", text="Direita").type='RIGHT'
        row.operator("view3d.viewnumpad", text="Esquerda").type='LEFT'
        
        row = layout.row()
        row.operator("view3d.viewnumpad", text="Cima").type='TOP'
        row.operator("view3d.viewnumpad", text="Baixo").type='BOTTOM'
        
        row = layout.row()
        row.operator("opr.pan_down_view1", text="Pan", icon="TRIA_UP")
        row.operator("opr.pan_up_view1", text="Pan", icon="TRIA_DOWN")
        row.operator("opr.pan_right_view1", text="Pan", icon="TRIA_LEFT")
        row.operator("opr.pan_left_view1", text="Pan", icon="TRIA_RIGHT")

        row = layout.row()
        row.operator("opr.orbit_down_view1", text="Orb", icon="FILE_PARENT")
        row.operator("opr.orbit_up_view1", text="Orb", icon="FILE_REFRESH")
        row.operator("opr.orbit_right_view1", text="Orb", icon="LOOP_BACK")
        row.operator("opr.orbit_left_view1", text="Orb", icon="LOOP_FORWARDS")

        
        row = layout.row()
        row.operator("view3d.view_persportho", text="Persp/Orto")
        row.operator("view3d.view_all", text="Centraliza Zoom", icon="VIEWZOOM").center=False    

# FOTOGRAMETRIA

class RhinCriaFotogrametria(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Cria Fotogrametria"
    bl_idname = "rhin_cria_fotogrametria"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"


    def draw(self, context):
        layout = self.layout
        scn = context.scene
        obj = context.object 
        
        col = layout.column(align=True)
        col.prop(scn.my_tool, "path", text="")
 
        row = layout.row()
        row.operator("object.rhin_gera_modelo_foto", text="Iniciar Fotogrametria", icon="IMAGE_DATA")

        row = layout.row()
        row.operator("object.gera_modelo_foto_smvs", text="SMVS+Meshlab", icon="IMAGE_DATA")

# IMPORTA FOTOGRAMETRIA

class RhinImportaFotogrametria(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Importar Fotogrametria"
    bl_idname = "rhin_importa_fotogrametria"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.operator("import_scene.obj", text="Importa OBJ", icon="MOD_MASK")

class RhinAlinhaFaces(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Alinha Faces"
    bl_idname = "rhin_alinha_faces"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        layout.operator("object.alinha_rosto", text="1 - Alinha com a Camera", icon="MANIPUL")
        col = self.layout.column(align = True)
        col.prop(context.scene, "medida_real")  
        layout.operator("object.alinha_rosto2", text="2 - Alinha e Redimensiona", icon="LAMP_POINT")

        layout.operator("object.rotaciona_z", text="Flip Z", icon="FORCE_MAGNETIC")


# ESTUDA FACE

class RhinEstudaFaces(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Estuda Faces"
    bl_idname = "rhin_estuda_faces"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        linha=row.operator("mesh.add_linhabase", text="Linha Central Ver", icon="PAUSE")
        linha.location=(0,-200,0)

        row = layout.row()
        linha=row.operator("mesh.add_linhabase", text="Linha Central Hor", icon="ZOOMOUT")
        linha.location=(0,-200,0)
        linha.rotation=(0,1.5708,0)
        
        row = layout.row()
        linha=row.operator("mesh.add_linhabase", text="Linha Lateral Hor", icon="ZOOMOUT")
        linha.location=(200,30,0)
        linha.rotation=(1.5708,0,0)
        
        row = layout.row()
        row.operator("view3d.snap_cursor_to_selected", text="Pivô para Seleção", icon="RESTRICT_SELECT_OFF")
        
        row = layout.row()
        row.operator("object.pivo_cursor", text="Pivô no Cursor", icon="CURSOR")


#        row = layout.row()
#        row.operator("object.align_picked_points", text="Alinha por Pontos", icon="PARTICLE_TIP")

        row = layout.row()        
        row.label(text="Gabarito:")


        row = layout.row()
        linha=row.operator("object.rhin_importa_med_nariz", text="Importar Medidas Nariz", icon="FULLSCREEN_ENTER")
        
        row = layout.row()
        row.operator("object.distancia_objetos", text="Atualiza Fator/Ãngulo", icon="STICKY_UVS_DISABLE")        

        row = layout.row()        
        row.label(text="Ferramentas de Medidas:")
        

        row = layout.row()
        row.operator("measureit.runopenglbutton", text="Ver/Ocultar Medidas", icon="ARROW_LEFTRIGHT")


        row = layout.row()
        row.operator("measureit.addsegmentbutton", text="Fazer Medida", icon="CURVE_NCURVE")

        row = layout.row()
        row.operator("measureit.addanglebutton", text="Medir Ângulo", icon="EDITMODE_VEC_DEHLT")
        
        row = layout.row()
        row.operator("view3d.ruler", text="Medida/Ângulo Rápido", icon="IPO_LINEAR")
        


# SEPARAR FACE
   
class RhinSeparaFace(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Separar Face"
    bl_idname = "rhin_separa_face"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        circle=row.operator("mesh.primitive_circle_add", text="Círculo de Corte", icon="MESH_CIRCLE")
        circle.radius=200
        circle.vertices=100
        circle.location=(135,-185,0)
        circle.rotation=(0,1.5708,0)
        
        row = layout.row()
        knife=row.operator("object.corta_face", text="Cortar!", icon="META_PLANE")
        
        row = layout.row()
        circle=row.operator("object.rosto_cria_copia", text="Copia Face", icon="NODETREE")
        
        
        
# ESCULPIR
      
class RhinEscultura(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Escultura"
    bl_idname = "rhin_escultura"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object


        row = layout.row()
        row.operator("object.mode_set", text="Modo Objeto", icon="OBJECT_DATA").mode = 'OBJECT'
        
        row = layout.row()
        row.operator("sculpt.sculptmode_toggle", text="Modo Escultura", icon="SCULPTMODE_HLT")
        
        row = layout.row()
        row.operator("object.escultura_grab", text="Agarra", icon="BRUSH_GRAB")
 
        row = layout.row()
        row.operator("paint.brush_select", text="Empurra", icon="BRUSH_NUDGE").sculpt_tool='NUDGE'
        
        row = layout.row()
        row.operator("paint.brush_select", text="Desenha", icon="BRUSH_SCULPT_DRAW").sculpt_tool='DRAW'
        
        row = layout.row()
        row.operator("paint.brush_select", text="Alisa", icon="BRUSH_SMOOTH").sculpt_tool='SMOOTH'

# SECÇÃO PRÉ E PÓS

def RhinPlanoSeccaoDef(self, context):
    
    context = bpy.context
    obj = context.active_object
    scn = context.scene

    plano = bpy.data.objects['PlanoSeccaoPrePos']
    corte = plano.location[0]

    face = bpy.data.objects['face']
    face_copia = bpy.data.objects['face_copia']
    

    bpy.ops.object.select_all(action='DESELECT')
    face.select = True
    face_copia.select = True
    bpy.context.scene.objects.active = face
    bpy.ops.object.duplicate()
    
    face1 = bpy.data.objects['face.001']
    face_copia1 = bpy.data.objects['face_copia.001']

# Cria a linha do pré
    bpy.ops.object.select_all(action='DESELECT')
    face1.select = True
    bpy.context.scene.objects.active = face1
  

    bpy.ops.object.mode_set(mode='EDIT')

    mesh=bmesh.from_edit_mesh(bpy.context.object.data)
    for v in mesh.verts:
        v.select = True

    bpy.ops.mesh.select_all(action='TOGGLE') # seleciona tudo
    bpy.ops.mesh.select_all(action='TOGGLE') # seleciona tudo

    bpy.ops.mesh.bisect(plane_co=(corte, 0, 0), plane_no=(1, 0, 0))
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT') # Depois de fazer tudo voltar ao modo de Objeto

# Cria a linha do pós

    bpy.ops.object.select_all(action='DESELECT')
    face_copia1.select = True
    bpy.context.scene.objects.active = face_copia1
  

    bpy.ops.object.mode_set(mode='EDIT')

    mesh=bmesh.from_edit_mesh(bpy.context.object.data)
    for v in mesh.verts:
        v.select = True

    bpy.ops.mesh.select_all(action='TOGGLE') # seleciona tudo
    bpy.ops.mesh.select_all(action='TOGGLE') # seleciona tudo

    bpy.ops.mesh.bisect(plane_co=(corte, 0, 0), plane_no=(1, 0, 0))
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT') # Depois de fazer tudo voltar ao modo de Objeto
    
# Deixa apenas as linhas do pré e pós selecionadas

    bpy.ops.object.select_all(action='DESELECT')
    face1.select = True
    face_copia1.select = True
    bpy.context.scene.objects.active = face1        

class RhinPlanoSeccao(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.rhin_plano_seccao"
    bl_label = "Cria linhas de secção"
    
    def execute(self, context):
        RhinPlanoSeccaoDef(self, context)
        return {'FINISHED'}

# PRE E PÓS

class RhinPrePos(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Pré e Pós"
    bl_idname = "rhin_pre_pos"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()        
        row.label(text="Pré x Pós Digital:")

        row = layout.row()


        row = layout.row()
        row.operator("object.mostra_oculta_face", text="Mostra/Oculta Face", icon="MOD_MASK")

        row = layout.row()
        row.operator("render.render_pre_pos", text="Imagem Pré e Pós", icon="META_ELLIPSOID")

        row = layout.row()
        circle=row.operator("mesh.rhin_plano_seccao", text="Plano de Secção", icon="MESH_PLANE")

        row = layout.row()
        row.operator("object.rhin_plano_seccao", text=" Cria Linhas Pré e Pós", icon="PARTICLE_PATH")

        row = layout.row()
        row.operator("view3d.clip_border", text="Cria Filete", icon="UV_FACESEL")
        
        row = layout.row()        
        row.label(text="Pós Digital x Pós Real:")
        
        row = layout.row()
        row.operator("object.align_picked_points", text="Alinha por Pontos", icon="PARTICLE_TIP")

        row = layout.row()
        row.operator("object.align_icp", text="Alinha por ICP", icon="PARTICLE_PATH")        

# DESENHA GUIA
   
class RhinDesenhaGuia(bpy.types.Panel):
    """Planejamento de cirurgia ortognática no Blender"""
    bl_label = "Desenha Guia"
    bl_idname = "rhin_desenha_guia"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rhin"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("cut_mesh.polytrim", text="Desenha Cortes", icon="OUTLINER_DATA_MESH")
        
        row = layout.row()
        circle=row.operator("object.cria_espessura", text="Cria Espessura", icon="MOD_SOLIDIFY")
        
        row = layout.row()
        row.operator("object.prepara_impressao", text="Prepara Impressão 3D", icon="MOD_REMESH")
        
 


def register():
    bpy.utils.register_class(RhinGeraModeloFoto)
    bpy.utils.register_class(RhinImportaMedNariz)
    bpy.utils.register_class(RhinCriaPlanoSeccao)
    bpy.utils.register_class(RhinMostraOcultaFace)
#    bpy.types.INFO_MT_mesh_add.append(add_object_button)
    bpy.utils.register_class(RhinPivoCursor)
    bpy.utils.register_class(RhinCriaEspessura)
    bpy.utils.register_class(RhinEsculturaGrab)
    bpy.utils.register_class(RhinRostoCriaCopia)
    bpy.utils.register_class(RhinRenderPrePos)
    bpy.utils.register_class(RhinDistanciaObjetos)
    bpy.utils.register_class(RhinZoomCena)
    bpy.utils.register_class(RhinCriaFotogrametria)
    bpy.utils.register_class(RhinImportaFotogrametria)
    bpy.utils.register_class(RhinAlinhaFaces)
    bpy.utils.register_class(RhinSeparaFace)
    bpy.utils.register_class(RhinEstudaFaces)
    bpy.utils.register_class(RhinEscultura)
    bpy.utils.register_class(RhinPlanoSeccao)
    bpy.utils.register_class(RhinPrePos)
    bpy.utils.register_class(RhinDesenhaGuia)

    

def unregister():
    bpy.utils.unregister_class(RhinGeraModeloFoto)
    bpy.utils.unregister_class(RhinImportaMedNariz)
    bpy.utils.unregister_class(RhinCriaPlanoSeccao)
    bpy.utils.unregister_class(RhinMostraOcultaFace)
#    bpy.types.INFO_MT_mesh_add.remove(add_object_button)
    bpy.utils.unregister_class(RhinPivoCursor)
    bpy.utils.unregister_class(RhinCriaEspessura)
    bpy.utils.unregister_class(RhinEsculturaGrab)
    bpy.utils.unregister_class(RhinRostoCriaCopia)
    bpy.utils.unregister_class(RhinRenderPrePos)
    bpy.utils.unregister_class(RhinDistanciaObjetos)
    bpy.utils.unregister_class(RhinZoomCena)
    bpy.utils.unregister_class(RhinCriaFotogrametria)
    bpy.utils.unregister_class(RhinImportaFotogrametria)
    bpy.utils.unregister_class(RhinAlinhaFaces)
    bpy.utils.unregister_class(RhinSeparaFace)
    bpy.utils.unregister_class(RhinEstudaFaces)
    bpy.utils.unregister_class(RhinEscultura)
    bpy.utils.unregister_class(RhinPlanoSeccao)
    bpy.utils.unregister_class(RhinPrePos)
    bpy.utils.unregister_class(RhinDesenhaGuia)


if __name__ == "__main__":
    register()
