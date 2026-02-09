import hou, platform

# KEY NAMES
# uparrow, downarrow, leftarrow, rightarrow
# alt, cmd, shift, ctrl, tab, del, backspace, enter, esc
# f1...f12
# pageup, pagedown, end, home, insert
# /, \\
# pad0...pad9
# padstar, padslash
# pause
# space

class Bindings:
    def __init__(self):
        return

    def load(self):
        self.clearAssignments()
        self.addAssignments()

    def clearAssignments(self):
        assignments = (
            #
            # deskmgr
            #
            'deskmgr.new',
            'deskmgr.save',
            #
            # h
            #
            'h.add_key',
            'h.aliases',
            'h.audio_panel',
            'h.auto_key',
            'h.cache_manager',
            'h.channeleditor',
            'h.clear_cop_caches',
            'h.comp_project_manager',
            'h.context_help',
            'h.desktop_mgr',
            'h.find',
            'h.global_animation_options',
            'h.mat_palette',
            'h.merge',
            'h.new',
            'h.next_key',
            'h.open',
            'h.perf_monitor',
            'h.python_shell',
            'h.textport',
            #
            # h.pane
            #
            'h.pane.clone',
            'h.pane.closetab',
            'h.pane.copytab',
            'h.pane.edit_bookmark',
            'h.pane.editpathastext',
            'h.pane.link_minus',
            'h.pane.link_plus',
            'h.pane.nexttab',
            'h.pane.prevtab',
            'h.pane.to_cop_view',
            'h.pane.to_chanedit',
            'h.pane.to_chop_view',
            'h.pane.to_geosheet',
            'h.pane.to_ipr_viewer',
            'h.pane.to_mat_palette',
            'h.pane.to_net',
            'h.pane.to_old_net',
            'h.pane.to_parm',
            'h.pane.to_scene_view',
            'h.pane.to_textport',
            'h.pane.to_treeview',
            #
            # h.pane.bundle
            #
            'h.pane.bundle.addbundle',
            'h.pane.bundle.duplicate',
            #
            # h.pane.chedit
            #
            'h.pane.chedit.bsave',
            'h.pane.chedit.load',
            'h.pane.chedit.save',
            'h.pane.chedit.scroll_to_current_frame',
            'h.pane.chedit.show_groups',
            'h.pane.chedit.show_layers',
            'h.pane.chedit.show_parmbox',
            #
            # h.pane.chlist
            #
            'h.pane.chlist.parmbox.show_filter',
            #
            # h.pane.group
            #
            'h.pane.group.addgroup',
            'h.pane.group.equals',
            'h.pane.group.minus',
            'h.pane.group.selectall',
            'h.pane.group.selectnone',
            'h.pane.group.togpin',
            'h.pane.group.togpinall',
            #
            # h.pane.gview
            #
            'h.pane.gview.increase_subd',
            'h.pane.gview.decrease_subd',
            'h.pane.gview.delete',
            'h.pane.gview.dockhudhandles',
            'h.pane.gview.edit_snap_options',
            'h.pane.gview.operator_menu_branch',
            'h.pane.gview.state.view.home_selection',
            'h.pane.gview.repeat_current',
            'h.pane.gview.repeat_current_branch',
            'h.pane.gview.restore_prevcam',
            'h.pane.gview.selectstylebox',
            'h.pane.gview.selectstylebrush',
            'h.pane.gview.selectstylelaser',
            'h.pane.gview.selectstylelasso',
            #
            # h.pane.gview.handle
            #
            'h.pane.gview.handle.remove_keyframe',
            'h.pane.gview.handle.set_keyframe',
            #
            # h.pane.gview.handle.agentcollisionlayer
            #
            'h.pane.gview.handle.agentcollisionlayer.boxhandle',
            'h.pane.gview.handle.agentcollisionlayer.orientationhandle',
            #
            # h.pane.gview.handle.agentconfigurejoints
            #
            'h.pane.gview.handle.agentconfigurejoints.conehandle',
            'h.pane.gview.handle.agentconfigurejoints.childrotationhandle',
            #
            # h.pane.gview.state
            #
            'h.pane.gview.state.volatile_chmodify',
            #
            # h.pane.wsheet
            #
            'h.pane.wsheet.change_wire_style',
            'h.pane.wsheet.add_image',
            'h.pane.wsheet.add_postit',
            'h.pane.wsheet.addfileop',
            'h.pane.wsheet.allowdroponwire',
            'h.pane.wsheet.batch_rename',
            'h.pane.wsheet.bypass_mode',
            'h.pane.wsheet.color_palette',
            'h.pane.wsheet.doautomovenodes',
            'h.pane.wsheet.dosnapping',
            'h.pane.wsheet.expose',
            'h.pane.wsheet.flag1_mode',
            'h.pane.wsheet.flag2_mode',
            'h.pane.wsheet.flag3_mode',
            'h.pane.wsheet.flag4_mode',
            'h.pane.wsheet.home',
            'h.pane.wsheet.home_selected',
            'h.pane.wsheet.up',
            'h.pane.wsheet.down',
            'h.pane.wsheet.left',
            'h.pane.wsheet.right',
            'h.pane.wsheet.edit_images',
            'h.pane.wsheet.layout',
            'h.pane.wsheet.layout_all',
            'h.pane.wsheet.layout_mode',
            'h.pane.wsheet.maximize',
            'h.pane.wsheet.maximize_adjust',
            'h.pane.wsheet.minimize',
            'h.pane.wsheet.minimize_adjust',
            'h.pane.wsheet.mode_switch',
            'h.pane.wsheet.node_quick_nav',
            'h.pane.wsheet.open_display_options',
            'h.pane.wsheet.open_groups',
            'h.pane.wsheet.open_treeview',
            'h.pane.wsheet.opmenu.flag_debug',
            'h.pane.wsheet.rename_node',
            'h.pane.wsheet.scope_chans',
            'h.pane.wsheet.select',
            'h.pane.wsheet.select_mode',
            'h.pane.wsheet.snap_netbox_bounds',
            'h.pane.wsheet.stitch_mode',
            'h.pane.wsheet.zoom_in',
            'h.pane.wsheet.zoom_out',
            #
            # h.playbar
            #
            'h.playbar.next_bookmark',
            'h.playbar.prev_bookmark',
            'h.playbar.show_range',
            #
            # inputfield
            #
            'inputfield.context_help',
            'inputfield.editor',
        )

        for assignment in assignments:
            context = assignment.rpartition('.')[0]
            symbol = assignment
            hou.hotkeys.clearAssignments(context, symbol)


    def addAssignments(self):
        assignments = (
            #
            # h
            #
            ('h.hc_panel', 'alt+shift+d'),
            ('h.stow_shelf', 'ctrl+]'),
            #
            # h.pane
            #
            ('h.pane.shelf',   'ctrl+['),
            ('h.pane.nexttab', 'ctrl+tab'),
            ('h.pane.prevtab', 'ctrl+shift+tab'),
            #
            # h.pane.gview
            #
            ('h.pane.gview.refplane',                  'shift+g'),
            ('h.pane.gview.state.view.home_selection', 'shift+s'),
            #
            # h.pane.parms
            #
            ('h.pane.parms.edit_expression', 'alt+e'),
            #
            # h.pane.editparms
            #
            ('h.pane.editparms.selectall', 'alt+h'),
            #
            # h.pane.wsheet
            #
            ('h.pane.wsheet.bypass_mode',       'q'),
            # ('h.pane.wsheet.desel_noncurrent',  'ctrl+d'),
            ('h.pane.wsheet.doautomovenodes',   'ctrl+pad9'),
            ('h.pane.wsheet.down',              'shift+j'),
            ('h.pane.wsheet.drop_on_wire_mode', 'pad8'),
            ('h.pane.wsheet.flag2_mode',        'w'),
            ('h.pane.wsheet.flag3_mode',        'e'),
            ('h.pane.wsheet.home_selected',     'shift+s'),
            ('h.pane.wsheet.jump_mark_1',       'pad1'),
            ('h.pane.wsheet.jump_mark_2',       'pad2'),
            ('h.pane.wsheet.jump_mark_3',       'pad3'),
            ('h.pane.wsheet.jump_mark_4',       'pad4'),
            ('h.pane.wsheet.jump_mark_5',       'pad5'),
            ('h.pane.wsheet.left',              'shift+h'),
            ('h.pane.wsheet.node_quick_nav',    'ctrl+f'),
            ('h.pane.wsheet.right',             'shift+l'),
            ('h.pane.wsheet.rename_node',       'ctrl+r'),
            ('h.pane.wsheet.set_mark_1',        'ctrl+pad1'),
            ('h.pane.wsheet.set_mark_2',        'ctrl+pad2'),
            ('h.pane.wsheet.set_mark_3',        'ctrl+pad3'),
            ('h.pane.wsheet.set_mark_4',        'ctrl+pad4'),
            ('h.pane.wsheet.set_mark_5',        'ctrl+pad5'),
            ('h.pane.wsheet.select',            'ctrl+a'),
            ('h.pane.wsheet.up',                'shift+k'),
            #
            # h.pane.textport
            #
            ('h.pane.textport.up',             'ctrl+p'),
            ('h.pane.textport.down',           'ctrl+n'),
            ('h.pane.textport.next',           'ctrl+f'),
            ('h.pane.textport.prev',           'ctrl+b'),
            ('h.pane.textport.top',            'ctrl+a'),
            ('h.pane.textport.bottom',         'ctrl+e'),
            ('h.pane.textport.nextword',       'alt+f'),
            ('h.pane.textport.pageup',         'alt+v'),
            ('h.pane.textport.pagedown',       'ctrl+v'),
            ('h.pane.textport.firstline',      'ctrl+shift+,'),
            ('h.pane.textport.lastline',       'ctrl+shift+.'),
            ('h.pane.textport.jump_to_line',   'alt+g'),
            ('h.pane.textport.selectup',       'ctrl+shift+p'),
            ('h.pane.textport.selectdown',     'ctrl+shift+n'),
            ('h.pane.textport.selectnext',     'ctrl+shift+f'),
            ('h.pane.textport.selectprev',     'ctrl+shift+b'),
            ('h.pane.textport.selectbottom',   'ctrl+shift+e'),
            ('h.pane.textport.selecttop',      'ctrl+shift+a'),
            ('h.pane.textport.selectnextword', 'alt+shift+f'),
            ('h.pane.textport.toggle_comment', 'ctrl+/'),
            #
            # inputfield
            #
            ('inputfield.up',        'ctrl+p'),
            ('inputfield.down',      'ctrl+n'),
            ('inputfield.next',      'ctrl+f'),
            ('inputfield.prev',      'ctrl+b'),
            ('inputfield.next_word', 'alt+f'),
            ('inputfield.prev_word', 'alt+b'),
            ('inputfield.end',       'ctrl+e'),
            ('inputfield.home',      'ctrl+a'),
        )

        for assignment in assignments:
            context = assignment[0].rpartition('.')[0]
            symbol = assignment[0]
            key = assignment[1]
            hou.hotkeys.addAssignment(context, symbol, key)


    def bindCommands(self):

        list = ()
        for command in list:
            context = binding[0]
            command = binding[1]
            hou.hotkeys.addCommandBinding(context, command)
