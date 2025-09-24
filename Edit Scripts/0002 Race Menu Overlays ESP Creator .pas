{
  Creates a RaceMenu plugin: ESP or ESP flagged as ESL, by duplicating a selected source plugin.
  Sets optional header fields (Author/Description) and copies all records with required masters.
  For QUST records, you can set a Papyrus script name (updates FULL, EDID and VMAD scriptName).
  After completion:
    1) Open the Quest and replace the FormID with the one from your own plugin.
    2) Apply "Clean Masters" on your project.
  An explanatory video can be opened at the end of the process.
  The code runs on hope and dreams.
  Author: John95AC
}

unit UserScript;

var
  sourceFile: IInterface;
  destinationFile: IInterface;
  didCopy: boolean;
  authorText: string;
  descText: string;
  edidPrefix: string;
  edidCount: Integer;
  navCount: Integer;

procedure SetHeaderStrings(f: IInterface; const author, desc: string);
var
  hdr: IInterface;
begin
  if not Assigned(f) then Exit;
  hdr := ElementByIndex(f, 0);
  if not Assigned(hdr) then Exit;

  if Trim(author) <> '' then
    SetElementEditValues(hdr, 'CNAM - Author', author);
  if Trim(desc) <> '' then
    SetElementEditValues(hdr, 'SNAM - Description', desc);
end;

function Initialize: integer;
begin
  Result := 0;
  sourceFile := nil;
  destinationFile := nil;
  didCopy := False;
  authorText := '';
  descText := '';
  edidPrefix := '';
  edidCount := 0;
  navCount := 0;
end;

function Process(e: IInterface): integer;
var
  frm: TForm;
  clb: TCheckListBox;
  i, j, k: integer;
  rec: IInterface;
  newRec: IInterface;
  src: IInterface;
  madeESL: boolean;
  hdr: IInterface;
  elEditorID: IInterface;
  s, s1: string;
  posSpace: Integer;
  zPos: Integer;
  initiallyDisabled, skipIt, isNavMesh: Boolean;
  sigStr: string;
  perSigCount: TStringList;
  nameFrom: string;
  baseEl: IInterface;
  baseRec: IInterface;
  countVal: Integer;
  outStr: string;
  vmad, scripts, scriptEntry: IInterface;
  
begin
  Result := 0;
  madeESL := False;

  
  src := GetFile(e);
  if not Assigned(sourceFile) then
    sourceFile := src;

  
  if (src <> sourceFile) or didCopy then Exit;

  
  frm := frmFileSelect;
  try
    frm.Caption := 'Select destination plugin (new recommended)';
    clb := TCheckListBox(frm.FindComponent('CheckListBox1'));
    clb.Items.Clear;
    clb.Items.Add('<new file>');
    clb.Items.Add('<new file - ESL flagged>');
    for i := 0 to Pred(FileCount) do
      clb.Items.InsertObject(2, GetFileName(FileByIndex(i)), FileByIndex(i));

    if frm.ShowModal <> mrOk then begin
      Result := 1;
      Exit;
    end;

    for i := 0 to Pred(clb.Items.Count) do
      if clb.Checked[i] then begin
        if i = 0 then begin
          destinationFile := AddNewFile;
        end else if i = 1 then begin
          destinationFile := AddNewFile;
          madeESL := True;
        end else begin
          destinationFile := ObjectToElement(clb.Items.Objects[i]);
        end;
        Break;
      end;
  finally
    frm.Free;
  end;

  if not Assigned(destinationFile) then begin
    Result := 1;
    Exit;
  end;

  
  SetHeaderStrings(destinationFile, authorText, descText);

  
  for i := 0 to Pred(RecordCount(sourceFile)) do begin
    rec := RecordByIndex(sourceFile, i);
    if not Assigned(rec) then
      Continue;

    
    AddRequiredElementMasters(rec, destinationFile, False);

    
    newRec := wbCopyElementToFile(rec, destinationFile, True, True);

    
    if Signature(rec) = 'QUST' then
    begin
      InputQuery('Papyrus Script Name', 'Enter the Papyrus script name (without extension, no spaces):', s);
      if Trim(s) <> '' then
      begin
       SetElementEditValues(newRec, 'FULL - Name', s);
       SetElementEditValues(newRec, 'EDID - Editor ID', '00' + s);
       vmad := ElementByPath(newRec, 'VMAD - Virtual Machine Adapter');
       if not Assigned(vmad) then
         vmad := Add(newRec, 'VMAD - Virtual Machine Adapter', True);
       if Assigned(vmad) then
       begin
         scripts := ElementByPath(vmad, 'Scripts');
         if not Assigned(scripts) then
           scripts := Add(vmad, 'Scripts', True);
         if Assigned(scripts) then
         begin
           if ElementCount(scripts) = 0 then
             scriptEntry := ElementAssign(scripts, HighInteger, nil, False)
           else
             scriptEntry := ElementByIndex(scripts, 0);
           if Assigned(scriptEntry) then
             SetElementEditValues(scriptEntry, 'scriptName', s);
         end;
       end;
      end; 
    end; 
  end;

  
  if madeESL then
  begin
    AddMessage('Re-applying ESL flag to header.');
    hdr := ElementByIndex(destinationFile, 0);
    if Assigned(hdr) then
    begin
      SetElementNativeValues(hdr, 'Record Header\Record Flags\ESL', 1);
    end
    else
    begin
      AddMessage('ERROR: Could not find header in destination file to apply ESL flag.');
    end;
  end;


  didCopy := True;
  AddMessage('Duplicated plugin: ' + GetFileName(sourceFile) + ' -> ' + GetFileName(destinationFile));

  
  if Trim(edidPrefix) <> '' then
  begin
    AddMessage('Running EDID pass on destination with prefix: ' + edidPrefix);
    perSigCount := TStringList.Create;
    perSigCount.Sorted := True;
    perSigCount.Duplicates := dupIgnore;
    for i := 0 to Pred(RecordCount(destinationFile)) do
    begin
      rec := RecordByIndex(destinationFile, i);
      if not Assigned(rec) then Continue;
      if Signature(rec) = 'TES4' then Continue;

      s1 := '';
      skipIt := False;
      sigStr := Signature(rec);
      isNavMesh := sigStr = 'NAVM';

      nameFrom := '';
      s := GetElementEditValues(rec, 'FULL - Name');
      if s <> '' then
      begin
        nameFrom := 'FULL';
      end
      else
      begin
        s := '';
        baseEl := ElementByPath(rec, 'NAME - Base');
        if Assigned(baseEl) then
        begin
          baseRec := LinksTo(baseEl);
          if Assigned(baseRec) then
          begin
            s := GetElementEditValues(baseRec, 'FULL - Name');
            if s <> '' then nameFrom := 'BASE.FULL' else
            begin
              s := GetElementEditValues(baseRec, 'EDID - Editor ID');
              if s <> '' then nameFrom := 'BASE.EDID';
            end;
          end;
        end;
      end;

      if s = '' then
        s := sigStr + '_' + IntToHex(GetLoadOrderFormID(rec), 8);

      posSpace := Pos(' ', s);
      if posSpace > 0 then s1 := Copy(s, 1, posSpace - 1) else s1 := s;
      if isNavMesh then s1 := 'Navigation Mesh';

      zPos := 0;
      initiallyDisabled := False;
      if ElementExists(rec, 'DATA\Position\Z') then
        zPos := GetElementNativeValues(rec, 'DATA\Position\Z');
      initiallyDisabled := GetIsInitiallyDisabled(rec);
      if (zPos = -30000) and initiallyDisabled then skipIt := True;

      elEditorID := ElementByName(rec, 'EDID - Editor ID');
      if Assigned(elEditorID) and skipIt then
        elEditorID := RemoveElement(rec, 'EDID');
      if not skipIt then
      begin
        for j := 1 to Length(s1) do
          if not (s1[j] in ['A'..'Z','a'..'z','0'..'9','_']) then s1[j] := '_';
        countVal := StrToIntDef(perSigCount.Values[sigStr], 0);

        if isNavMesh then
        begin
          outStr := s1 + '_' + IntToStr(navCount);
          Inc(navCount);
        end
        else
        begin
          outStr := edidPrefix + s1 + '_' + IntToStr(countVal);
          Inc(countVal);
          perSigCount.Values[sigStr] := IntToStr(countVal);
        end;
        SetElementEditValues(rec, 'EDID - Editor ID', outStr);
      end;
    end;
    perSigCount.Free;
  end;
end;

function Finalize: integer;
var
  frm: TForm;
  lbl: TLabel;
  btn: TButton;
  img: TImage;
  imgPath: string;
  btnPlay: TButton;
  res: Integer;
  aviPath: string;
begin
  Result := 0;
  if Assigned(destinationFile) then
  begin
    AddMessage('Done. Destination: ' + GetFileName(destinationFile));
    
    frm := TForm.Create(nil);
    try
      frm.Caption := 'Script Completado';
      frm.Width := 640;
      frm.Height := 320;
      frm.Position := poScreenCenter;
    
      lbl := TLabel.Create(frm);
      lbl.Parent := frm;
      lbl.Caption := 'Congratulations! Your plugin has been created.' + #13#10 +
                     'Next steps:' + #13#10 +
                     '1) Open the Quest and in FormID replace it with the FormID from your own plugin.' + #13#10 +
                     '2) Apply "Clean Masters" on your project.' + #13#10 +
                     'Watch the video to see the complete process.' + #13#10 +
                     'The code runs on hope and dreams.';
      lbl.Left := 20;
      lbl.Top := 20;
      lbl.Width := 600;
      lbl.Height := 160;
      lbl.WordWrap := True;
      lbl.Font.Name := 'Segoe UI';
      lbl.Font.Size := 14;
      lbl.Font.Style := [fsBold];
    
      btn := TButton.Create(frm);
      btn.Parent := frm;
      btn.Caption := 'Cerrar';
      btn.Left := 340;
      btn.Top := 240;
      btn.Width := 120;
      btn.Height := 36;
      btn.ModalResult := mrOk;
    
      btnPlay := TButton.Create(frm);
      btnPlay.Parent := frm;
      btnPlay.Caption := 'Open video (MP4)';
      btnPlay.Left := 480;
      btnPlay.Top := 240;
      btnPlay.Width := 130;
      btnPlay.Height := 36;
      btnPlay.ModalResult := mrYes;
      
      res := frm.ShowModal;
      if res = mrYes then
      begin
        aviPath := ProgramPath + 'Edit Scripts\012.mp4';
        AddMessage('Opening MP4 externally: ' + aviPath);
        try
          ShellExecute(0, 'open', PChar(aviPath), nil, nil, 1);
        except
          on E: Exception do
            AddMessage('Failed to open MP4 externally: ' + E.Message);
        end;
      end;
    finally
      frm.Free;
    end;
  end;
end;

end. 
