import bpy

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Kouda Ayu",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# メニュー項目描画
def draw_menu_manual(self, context):
    # self : 呼び出し元のクラスインスタンス
    # context : カーソルを合わせたときのポップアップのカスタマイズなどに使用
    
    # トップバーの「ヘルプメニュー」に項目(オペレータ)を追加
    self.layout.operator("wm.url_open_preset", text="Manual", icon="HELP")

# オペレータ 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばすオペレータ"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER', 'UNDO'}
    
    #メニューを実行した時に呼ばれるコールバック関数
    def execute(self, context):
        bpy.data.objects['Cube'].data.vertices[0].co.x += 1.0 
        print("頂点を伸ばした")

        #オペレータの命令終了を通知
        return {'FINISHED'}

# オペレータ ICO球を追加
class MYADDON_OT_add_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_add_ico_sphere"
    bl_label = "ICO球を追加"
    bl_description = "ICO球を追加するオペレータ"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER', 'UNDO'}
    
    #メニューを実行した時に呼ばれるコールバック関数
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を追加した")

        #オペレータの命令終了を通知
        return {'FINISHED'}

# トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #Blenderがクラスを認識する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "Mymenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by " + bl_info["author"]

    # サブメニューの描画
    def draw(self,context):

        #トップバーの「エディターメニュー」に項目(オペレータ)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
                              text=MYADDON_OT_stretch_vertex.bl_label)
        
        self.layout.operator(MYADDON_OT_add_ico_sphere.bl_idname,
                             text=MYADDON_OT_add_ico_sphere.bl_label)

    # 既存のメニューにサブメニューを追加
    def submenu(self,context):

        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)



# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_stretch_vertex,
    TOPBAR_MT_my_menu,
)


# アドオン有効化時コールバック
def register():
    # Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)

    # 「TOPBAR_MT_editor_menus」に変更して、トップバーに直接追加する
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました。")

# アドオン無効化時コールバック
def unregister():
    # 削除側も同じに合わせる
    # メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    
    # Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    print("レベルエディタが無効化されました。")

    



# テスト実行用コード
if __name__ == "__main__":
    register()