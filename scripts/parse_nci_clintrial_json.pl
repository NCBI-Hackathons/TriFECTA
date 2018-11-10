#!/usr/bin/perl -w
#collect_civic_data.pl

use LWP::UserAgent;
use JSON;
my %diags;
open ONCOTREE, "<Unique_Synonyms.csv" or die $!;
while (my $line = <ONCOTREE>) {
    chomp($line);
    my ($num,$oncocode,$diagnosis) = split(/,/,$line);
    push @{$otree{$oncocode}}, $diagnosis;
    $diag{$diagnosis} = $oncocode;
}
open DIAG, "<diagnosis.txt" or die $!;
while (my $line = <DIAG>) {
    chomp($line);
    my ($oncocode,$diagnosis) = split(/\t/,$line);
    $diagnosis =~ s/\"//g;
    push @{$otree{$oncocode}}, $diagnosis;
}
open OUT, ">clinicaltrialdb_bygene.txt" or die $!;
print OUT join("\t",'NCT','Phase','Conditions','Drugs','BriefTitle','OfficialTrial','Oncotree Codes'),"\n";

my @jsonfiles = `ls /project/hackathon/hackers11/shared/byGeneXML/*.xml`;
chomp(@jsonfiles);
foreach $jfile (@jsonfiles) {
    my $json_string = `cat $jfile`;
    $json_hash = decode_json($json_string);
    %hash = %{$json_hash};
    my $total = $hash{'total'};
    my @trials = @{$hash{trials}};
    foreach $trials (@trials) {
	my %thash = %{$trials};
	my %oncotree;
	my @conditions;
      F1:foreach $disease (@{$trials->{'diseases'}}) {
	  $cond = $disease->{'display_name'};
	  push @conditions, $cond;
	  if ($diag{$cond}) {
	      $oncotree{$diag{$cond}} = 1;
	      next F1;
	  }
	  foreach $ocode (keys %otree) {
	      foreach $diag (@{$otree{$ocode}}) {
		  if ($diag =~ m/$cond/i) {
		      $oncotree{$ocode} = 1 if (length($ocode) > 1) ;
		  }elsif ($cond =~ m/$diag/i) {
		      $oncotree{$ocode} = 1 if (length($ocode) > 1) ;
		  }
	      }
	  }
      }
	my @oncotreecodes = keys %oncotree;
	
	print OUT join("\t",$thash{nct_id},$thash{'phase'}{'phase'},join("|",@conditions),
		       '',$thash{'brief_title'},$thash{'official_title'},
		       join("|",keys %oncotree)),"\n";
    }
}
