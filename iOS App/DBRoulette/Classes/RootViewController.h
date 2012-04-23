//
//  RootViewController.h
//  DBRoulette
//
//  Created by Brian Smith on 6/29/10.
//  Copyright Dropbox, Inc. 2010. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <OpenTok/Opentok.h>


@class DBRestClient;


@interface RootViewController : UIViewController <UINavigationControllerDelegate, UIImagePickerControllerDelegate,OTSessionDelegate, OTSubscriberDelegate, OTPublisherDelegate> {
    UIButton* linkButton;
    UIViewController* photoViewController;
	DBRestClient* restClient;
    UIButton* takepic;

}

- (IBAction)didPressLink;
- (IBAction)didPresspic;

@property (nonatomic, retain) IBOutlet UIButton* linkButton;
@property (nonatomic, retain) UIViewController* photoViewController;
- (void)doConnect;
- (void)doDisconnect;
- (void)doPublish;
- (void)doUnpublish;
- (void)createUI;
- (void)setStatusLabel;

@end
